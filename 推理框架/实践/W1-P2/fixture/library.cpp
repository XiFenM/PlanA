#include "api.hpp"

// 同一源码构建两个版本，二者使用相同 SONAME。
#if P2_VARIANT == 1
int compute(int value) {
    return value * 2;
}
#elif P2_VARIANT == 2
double compute(double value) {
    return value * 3.0;
}
#else
#error "请通过构建工具指定 P2_VARIANT"
#endif
