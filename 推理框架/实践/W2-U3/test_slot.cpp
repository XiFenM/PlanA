#include <algorithm>
#include <array>
#include <condition_variable>
#include <cstddef>
#include <cstdint>
#include <exception>
#include <functional>
#include <iostream>
#include <mutex>
#include <set>
#include <stdexcept>
#include <string>
#include <thread>
#include <utility>
#include <vector>

#ifndef SLOT_HEADER
#define SLOT_HEADER "slot.hpp"
#endif
#include SLOT_HEADER

// W2-U3-P1 revision 1 的公开行为测试，不规定 SingleSlot 的内部状态表示。
// 每个 --case 由 harness 放在独立进程中运行；超时只检查能否收尾，不考速度。
// 下列同步对象属于测试夹具，不是 SingleSlot 的实现提示或组成部分。
namespace {

class TestFailure : public std::runtime_error {
 public:
  using std::runtime_error::runtime_error;
};

void require(bool condition, const std::string& message) {
  if (!condition) {
    throw TestFailure(message);
  }
}

std::string exception_text(std::exception_ptr error) {
  try {
    std::rethrow_exception(error);
  } catch (const std::exception& e) {
    return e.what();
  } catch (...) {
    return "非 std::exception 异常";
  }
}

// mark 只记录夹具明确执行过的动作。例如 *_entry 位于方法调用之前，
// 不声称线程已经进入 SingleSlot 内部，更不声称它已在 condition_variable 上等待。
class Events {
 public:
  void mark(const std::string& name) {
    {
      std::lock_guard<std::mutex> lock(mutex_);
      seen_.insert(name);
    }
    condition_.notify_all();
  }

  bool wait(const std::string& name) {
    std::unique_lock<std::mutex> lock(mutex_);
    condition_.wait(lock, [&] { return cancelled_ || seen_.count(name) != 0; });
    return seen_.count(name) != 0;
  }

  bool has(const std::string& name) {
    std::lock_guard<std::mutex> lock(mutex_);
    return seen_.count(name) != 0;
  }

  void cancel() {
    {
      std::lock_guard<std::mutex> lock(mutex_);
      cancelled_ = true;
    }
    condition_.notify_all();
  }

 private:
  std::mutex mutex_;
  std::condition_variable condition_;
  std::set<std::string> seen_;
  bool cancelled_ = false;
};

// 后台异常必须保留原文，包括 TODO: SingleSlot::<method>。
// 失败时先解除夹具自己的等待，再尝试 close 和 join，避免用 terminate 或
// 永远等不到 reader 检查点的超时掩盖未实现异常。错误实现若在自身方法里死锁，
// 则仍由进程级超时报告，不把任意用户代码强行 detach 后继续访问栈对象。
class Run {
 public:
  explicit Run(SingleSlot& slot) : slot_(slot) {}

  ~Run() {
    if (!joined_) {
      events.cancel();
      close_for_cleanup();
      join_all();
    }
  }

  template <typename Function>
  void start(std::string name, Function function) {
    threads_.emplace_back([this, name = std::move(name), function = std::move(function)]() mutable {
      try {
        function();
      } catch (...) {
        remember(name, std::current_exception());
        events.cancel();
        close_for_cleanup();
      }
    });
  }

  void wait(const std::string& event) {
    if (!events.wait(event)) {
      finish();
      throw TestFailure("夹具已取消，未到达检查点：" + event);
    }
  }

  void finish() {
    join_all();
    std::lock_guard<std::mutex> lock(errors_mutex_);
    if (!errors_.empty()) {
      throw TestFailure(errors_.front().first + ": " + exception_text(errors_.front().second));
    }
  }

  Events events;

 private:
  void remember(std::string where, std::exception_ptr error) {
    std::lock_guard<std::mutex> lock(errors_mutex_);
    errors_.emplace_back(std::move(where), error);
  }

  void close_for_cleanup() {
    try {
      slot_.close();
    } catch (...) {
      remember("失败收尾时 close", std::current_exception());
    }
  }

  void join_all() {
    if (joined_) {
      return;
    }
    for (auto& thread : threads_) {
      if (thread.joinable()) {
        thread.join();
      }
    }
    joined_ = true;
  }

  SingleSlot& slot_;
  std::vector<std::thread> threads_;
  std::mutex errors_mutex_;
  std::vector<std::pair<std::string, std::exception_ptr>> errors_;
  bool joined_ = false;
};

std::array<Batch, 3> batches() {
  return {Batch{3, 5, 7, 9}, Batch{10, -2, 8, 4}, Batch{-5, 0, 13, 42}};
}

// reader 只记录观察，不在回调中抛断言、不重入 slot，也不保存借用地址。
// 对 consume 返回值的断言放在回调外。上界用来报告重复交付，避免坏实现
// 一直返回 true 而只留下无信息的超时。
void consume_stream(SingleSlot& slot, const Reader& reader,
                    std::vector<bool>& results, std::size_t required_batches,
                    std::size_t maximum_batches) {
  for (std::size_t i = 0; i <= maximum_batches; ++i) {
    const bool consumed = slot.consume(reader);
    results.push_back(consumed);
    if (!consumed) {
      // 过早结束已是行为错误；关闭只用于让另一侧有机会收尾。
      if (i < required_batches) {
        slot.close();
      }
      return;
    }
  }
  throw TestFailure("consume 超过允许批次数仍返回 true，没有结束消费");
}

void check_consume_results(const std::vector<bool>& actual, std::size_t count) {
  std::vector<bool> expected(count, true);
  expected.push_back(false);
  require(actual == expected, "consume 应为每批返回一次 true，关闭并读尽后返回 false");
}

void normal_delivery(bool producer_first) {
  SingleSlot slot;
  const auto input = batches();
  std::vector<bool> accepted;
  std::vector<bool> consumed;
  std::vector<Batch> observed;
  // Run 放在所有被线程引用的局部变量之后，异常离开时先 join，再销毁这些变量。
  Run run(slot);

  auto producer = [&] {
    for (std::size_t i = 0; i < input.size(); ++i) {
      {
        Batch source = input[i];
        accepted.push_back(slot.publish(source));
        // publish 成功返回以后，调用者可以改写并销毁原输入。
        std::fill(source.begin(), source.end(), -999);
      }
      if (producer_first && i == 0) {
        run.events.mark("first_publish_returned");
        if (!run.events.wait("allow_remaining_publications")) {
          return;
        }
      }
    }
    slot.close();
  };

  auto consumer = [&] {
    run.events.mark("consumer_call_entry");
    consume_stream(slot, [&](const Batch& batch) { observed.push_back(batch); },
                   consumed, input.size(), input.size());
  };

  if (producer_first) {
    run.start("producer", producer);
    run.wait("first_publish_returned");
    require(accepted.front(), "首批在开放的空槽上应被接受");
    run.start("consumer", consumer);
    run.events.mark("allow_remaining_publications");
  } else {
    run.start("consumer", consumer);
    run.wait("consumer_call_entry");
    // 这里只控制消费者先到调用入口，不假设它已经进入内部 wait。
    run.start("producer", producer);
  }
  run.finish();

  require(accepted == std::vector<bool>(input.size(), true), "正常交付中有批次被拒绝");
  require(observed == std::vector<Batch>(input.begin(), input.end()),
          "三批输入应按接受顺序各交付一次，不能丢批、重复、混批或借用原输入");
  check_consume_results(consumed, input.size());
}

void normal_producer_first() { normal_delivery(true); }
void normal_consumer_first() { normal_delivery(false); }

void borrow_stable_reuse() {
  SingleSlot slot;
  const auto input = batches();
  std::array<bool, 2> accepted{false, false};
  std::vector<bool> consumed;
  std::vector<Batch> observed;
  Batch before;
  Batch after;
  bool same_storage = false;
  bool accepted_before_reader_release = false;
  Run run(slot);

  run.start("producer", [&] {
    {
      Batch source = input[0];
      accepted[0] = slot.publish(source);
    }
    run.events.mark("first_publish_returned");
    if (!run.events.wait("allow_second_publication")) {
      return;
    }
    run.events.mark("second_publish_entry");
    accepted[1] = slot.publish(input[1]);
    accepted_before_reader_release = accepted[1] && !run.events.has("release_reader");
    slot.close();
  });

  run.wait("first_publish_returned");
  require(accepted[0], "首批应被接受");
  run.start("consumer", [&] {
    consume_stream(slot, [&](const Batch& batch) {
      if (observed.empty()) {
        before = batch;
        const auto* address = batch.data();
        const auto count = batch.size();
        run.events.mark("reader_checkpoint");
        if (!run.events.wait("release_reader")) {
          return;
        }
        after = batch;
        same_storage = address == batch.data() && count == batch.size();
      }
      observed.push_back(batch);
    }, consumed, 2, 2);
  });

  run.wait("reader_checkpoint");
  run.events.mark("allow_second_publication");
  run.wait("second_publish_entry");
  // 不用 sleep 或“暂时没返回”证明阻塞，也不等待第二次 publish 返回才放行 reader。
  // 本测试给出一个受控交接机会；完整不变量仍需结合学习者代码 Review。
  run.events.mark("release_reader");
  run.finish();

  require(!accepted_before_reader_release, "reader 仍停在检查点时，下一批已被提前接受");
  require(before == input[0] && after == input[0] && same_storage,
          "reader 借用期间本批内容、大小和元素地址应保持有效且稳定");
  require(accepted[1], "reader 返回后，开放的槽应允许下一批发布");
  require(observed == std::vector<Batch>{input[0], input[1]}, "复用后两批数据不匹配");
  check_consume_results(consumed, 2);
}

void close_empty() {
  SingleSlot slot;
  bool result = true;
  std::size_t callback_count = 0;
  Run run(slot);
  run.start("consumer", [&] {
    run.events.mark("consumer_call_entry");
    result = slot.consume([&](const Batch&) { ++callback_count; });
  });
  run.wait("consumer_call_entry");
  slot.close();
  run.finish();
  require(!result && callback_count == 0, "空槽关闭后 consume 应返回 false，不调用 reader");
}

void close_before_workers() {
  SingleSlot slot;
  const Batch input{3, 5, 7, 9};
  bool accepted = true;
  bool consumed = true;
  std::size_t callback_count = 0;
  Run run(slot);

  // 先让 close 返回，再启动两个工作线程；线程之间不附加启动顺序。
  slot.close();
  run.start("producer", [&] { accepted = slot.publish(input); });
  run.start("consumer", [&] {
    consumed = slot.consume([&](const Batch&) { ++callback_count; });
  });
  run.finish();

  // 只在 join 后读取各线程的结果；不依赖 sleep 或额外唤醒来促成退出。
  std::cout << "publish=" << (accepted ? "true" : "false")
            << " consume=" << (consumed ? "true" : "false")
            << " reader_calls=" << callback_count << " joined=true\n";
  require(!accepted, "线程启动前空槽已关闭，publish 应返回 false");
  require(!consumed && callback_count == 0,
          "线程启动前空槽已关闭，consume 应返回 false 且不调用 reader");
}

void close_ready() {
  SingleSlot slot;
  const auto input = batches();
  {
    Batch source = input[0];
    require(slot.publish(source), "关闭前应接受首批");
  }
  slot.close();
  slot.close();
  require(!slot.publish(input[1]), "close 生效后应拒绝新批");

  std::vector<Batch> observed;
  const bool first = slot.consume([&](const Batch& batch) { observed.push_back(batch); });
  const bool exhausted = slot.consume([&](const Batch& batch) { observed.push_back(batch); });
  require(first && !exhausted && observed == std::vector<Batch>{input[0]},
          "关闭和重复关闭不能丢弃已接受批次；读尽后 consume 返回 false");
}

void close_full_publisher() {
  SingleSlot slot;
  const auto input = batches();
  std::array<bool, 2> accepted{false, true};
  Run run(slot);
  run.start("producer", [&] {
    accepted[0] = slot.publish(input[0]);
    run.events.mark("first_publish_returned");
    if (!run.events.wait("allow_second_publication")) {
      return;
    }
    run.events.mark("second_publish_entry");
    accepted[1] = slot.publish(input[1]);
  });
  run.wait("first_publish_returned");
  require(accepted[0], "首批应填入开放的空槽");
  run.events.mark("allow_second_publication");
  run.wait("second_publish_entry");
  // 此前没有消费者腾空槽位，因此第二批即使先到调用入口，也不应已被接受。
  slot.close();
  run.finish();
  require(!accepted[1], "满槽发布应能因关闭返回 false，而不是覆盖第一批或永久等待");

  std::vector<Batch> observed;
  const bool first = slot.consume([&](const Batch& batch) { observed.push_back(batch); });
  const bool exhausted = slot.consume([&](const Batch& batch) { observed.push_back(batch); });
  require(first && !exhausted && observed == std::vector<Batch>{input[0]},
          "满槽关闭后，第一批仍应恰好消费一次");
}

void close_reading() {
  SingleSlot slot;
  const auto input = batches();
  std::array<bool, 2> accepted{false, false};
  std::vector<bool> consumed;
  std::vector<Batch> observed;
  Batch before;
  Batch after;
  bool same_storage = false;
  bool accepted_before_reader_release = false;
  Run run(slot);

  run.start("producer", [&] {
    accepted[0] = slot.publish(input[0]);
    run.events.mark("first_publish_returned");
    if (!run.events.wait("allow_second_publication")) {
      return;
    }
    run.events.mark("second_publish_entry");
    accepted[1] = slot.publish(input[1]);
    accepted_before_reader_release = accepted[1] && !run.events.has("release_reader");
  });
  run.wait("first_publish_returned");
  require(accepted[0], "首批应被接受");
  run.start("consumer", [&] {
    consume_stream(slot, [&](const Batch& batch) {
      if (observed.empty()) {
        before = batch;
        const auto* address = batch.data();
        const auto count = batch.size();
        run.events.mark("reader_checkpoint");
        if (!run.events.wait("release_reader")) {
          return;
        }
        after = batch;
        same_storage = address == batch.data() && count == batch.size();
      }
      observed.push_back(batch);
    }, consumed, 1, 2);
  });

  run.wait("reader_checkpoint");
  run.events.mark("allow_second_publication");
  run.wait("second_publish_entry");
  run.start("closer", [&] {
    run.events.mark("close_call_entry");
    slot.close();
  });
  run.wait("close_call_entry");
  // close 可以因为 reader 全程持锁而尚未返回。主控独立释放 reader，
  // 不形成“close 等 reader，而 reader 的放行又等 close 返回”的夹具死锁。
  run.events.mark("release_reader");
  run.finish();

  require(!accepted_before_reader_release, "关闭竞争中，reader 仍占用数据时下一批已被接受");
  require(before == input[0] && after == input[0] && same_storage,
          "close 不能提前清理或覆盖正在借用的第一批");
  std::vector<Batch> expected{input[0]};
  if (accepted[1]) {
    // publish 与 close 竞争时允许发布先于关闭生效；这种情况下第二批必须被 drain。
    expected.push_back(input[1]);
  }
  require(observed == expected, "关闭时应处理所有已接受批次，且不得重复消费");
  check_consume_results(consumed, expected.size());
  require(!slot.publish(input[2]), "close 返回且线程结束后仍应拒绝新批");
}

struct Case {
  const char* name;
  void (*run)();
};

const std::array<Case, 8> cases{{
    {"normal_producer_first", normal_producer_first},
    {"normal_consumer_first", normal_consumer_first},
    {"borrow_stable_reuse", borrow_stable_reuse},
    {"close_empty", close_empty},
    {"close_ready", close_ready},
    {"close_full_publisher", close_full_publisher},
    {"close_reading", close_reading},
    {"close_before_workers", close_before_workers},
}};

}  // namespace

int main(int argc, char** argv) {
  if (argc == 2 && std::string(argv[1]) == "--list") {
    for (const auto& test : cases) {
      std::cout << test.name << '\n';
    }
    return 0;
  }
  if (argc != 3 || std::string(argv[1]) != "--case") {
    std::cerr << "用法：test_slot --list | --case NAME\n";
    return 2;
  }
  const std::string name = argv[2];
  const auto chosen = std::find_if(cases.begin(), cases.end(),
                                   [&](const Case& test) { return name == test.name; });
  if (chosen == cases.end()) {
    std::cerr << "未知 case：" << name << '\n';
    return 2;
  }
  try {
    chosen->run();
    std::cout << "PASS " << name << '\n';
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "FAIL " << name << ": " << error.what() << '\n';
    return 1;
  } catch (...) {
    std::cerr << "FAIL " << name << ": 非 std::exception 异常\n";
    return 1;
  }
}
