#pragma once

#include <condition_variable>
#include <cstdint>
#include <functional>
#include <mutex>
#include <stdexcept>
#include <vector>

// 学习者文件：只填写这里的核心实现。
// 约定：计划/八周冲刺进度/历史记录/W2-学习验收记录.md
//       #w2-u3-p1-contract-r1
// 测试负责创建线程、提供输入和回调，并在线程结束后销毁 SingleSlot。
using Batch = std::vector<std::int32_t>;
using Reader = std::function<void(const Batch&)>;

class SingleSlot {
 public:
  SingleSlot() : bs(BufferStatus::FREE), status(RunningStatus::RUNNING) {}
  // 接受一批四元素输入后返回 true；关闭后拒绝并返回 false。
  // 接受成功后，调用者可以修改或释放原输入。
  bool publish(const Batch& batch) {
    {
      std::unique_lock<std::mutex> lk(m);
      cv_producer.wait(lk, [&]{return (bs == BufferStatus::FREE) || (status == RunningStatus::CLOSING);});
      if (status == RunningStatus::CLOSING){
        return false;
      }
      std::size_t len = batch.size();
      B.resize(len);
      bs = BufferStatus::WRITING;
      for(std::size_t i = 0; i < len; i ++) {
        B[i] = batch[i];
      }
      bs = BufferStatus::READY;
    }
    cv_consumer.notify_one();
    return true;
  }

  // reader 同步借用槽内数据；返回前，本批内容与存储必须有效。
  // 处理一批返回 true；关闭且没有剩余批次时返回 false。
  bool consume(const Reader& reader) {
    {
      std::unique_lock<std::mutex> lk(m);
      cv_consumer.wait(lk, [&]{return (bs == BufferStatus::READY) || (status == RunningStatus::CLOSING && bs == BufferStatus::FREE);});
      if (status == RunningStatus::CLOSING && bs == BufferStatus::FREE){
        return false;
      } 
      bs = BufferStatus::READING;
      reader(B);
      bs = BufferStatus::FREE;
    }
    cv_producer.notify_one();
    return true;
  }

  // 停止接受新批，使等待者能够收尾；已接受批次仍须处理。
  // 可以等待状态锁；不要求立即返回。重复调用应安全。
  void close() {
    {
      std::lock_guard<std::mutex> lk(m);
      status = RunningStatus::CLOSING;
    }
    cv_producer.notify_all();
    cv_consumer.notify_all();
  }

 private:
  // TODO：由你选择并添加所需的数据、状态和同步成员。
  // 可以采用不同的正确实现，不要求照搬课程里的状态表示。
  Batch B;
  std::mutex m;
  std::condition_variable cv_producer, cv_consumer;
  enum class BufferStatus {
    FREE,
    WRITING,
    READY,
    READING
  } bs;
  enum class RunningStatus {
    RUNNING,
    CLOSING
  } status;
};
