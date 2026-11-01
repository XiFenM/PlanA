#include <condition_variable>
#include <cstddef>
#include <cstdint>
#include <iostream>
#include <memory>
#include <mutex>
#include <thread>

// W2-U3-P1：按学习者提出的方案，将释放移到 consumer.join() 之后。
// 这里只演示一次延迟读取，不实现单槽队列或关闭协议。
int main() {
    constexpr std::size_t count = 4;
    auto payload = std::make_unique<std::int32_t[]>(count);
    for (std::size_t i = 0; i < count; ++i) {
        payload[i] = static_cast<std::int32_t>(2 * i + 3);
    }
    const std::int32_t* borrowed = payload.get();

    // 同步对象、信号与结果都由 main 持有，直到线程 join 后才离开作用域。
    std::mutex mutex;
    std::condition_variable cv;
    bool start_read = false;
    std::int64_t observed_sum = 0;

    // 地址按值带入线程；start_read 的全部访问都在同一个 mutex 下。
    std::thread consumer([&, borrowed] {
        {
            std::unique_lock lock(mutex);
            cv.wait(lock, [&] { return start_read; });
        }
        // wait 返回后才访问元素；计算期间不再访问 start_read。
        for (std::size_t i = 0; i < count; ++i) {
            observed_sum += borrowed[i];
        }
    });

    // main 继续持有数据，先发布允许读取的信号。
    {
        std::lock_guard lock(mutex);
        start_read = true;
    }
    cv.notify_one();

    consumer.join();
    // join 返回确认消费者已结束读取，此时才释放元素存储。
    payload.reset();
    // main 只在线程结束后读取结果。
    std::cout << "observed_sum=" << observed_sum << '\n';
}
