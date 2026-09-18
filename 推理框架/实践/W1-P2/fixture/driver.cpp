#include "api.hpp"

#include <iostream>
#include <string>
#include <unistd.h>

int main() {
    // 给检查目标 PID 映射留出位置；尚未调用 compute。
    std::cout << "READY pid=" << getpid() << std::endl;
    std::string command;
    if (!std::getline(std::cin, command) || command != "call") {
        std::cerr << "需要输入 call 才执行目标函数\n";
        return 2;
    }
    const int result = compute(7);
    std::cout << "RESULT " << result << std::endl;
    return result == 14 ? 0 : 3;
}
