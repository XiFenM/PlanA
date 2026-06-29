 

# Pytorch-1 基本内部机制

## 资料来源

1. **Ezyang "PyTorch Internals"（2019 经典）**
   - 链接：https://blog.ezyang.com/2019/05/pytorch-internals/
2. **Pytorch 官方文档——stride章节**
   - 链接：https://docs.pytorch.org/docs/2.12/generated/torch.Tensor.stride.html

## 先猜再学

《PyTorch Internals》（PyTorch 内部机制）是由 PyTorch 核心开发者 Edward Z. Yang 所写的一篇经典技术博客，深入剖析了 PyTorch 底层架构、张量存储、派发系统及自动微分的运作原理。学习这篇文章对于我们了解 Pytorch 的基本功能很有帮助。但是由于文章写于2019年，时间较早，所以许多技术细节可能已经发生变迁而且缺少一些Pytorch2.0以来的一些新特性。我们不必死记硬背其中细节，重点了解思想即可。

### 当前状态背景

关于Pytorch，我个人的背景是很熟悉的。在我工作中，Pytorch处于核心枢纽地位：向上面向深度学习训练、推理等各种框架应用程序，向下对接我们自研芯片的高性能算子库、通信库、运行时等底层软件工具包。于是，为了满足需求与调试问题，常常需要深入Pytorch源代码进行魔改和修复。其中，对于ProcessGroup通信组和添加自定义新算子最为熟悉，一方面是因为主导了对自定义ProcessGroup的适应性魔改，另一方面是为了适配各种新模型而添加大量自定义新算子。

### 期望回答的问题

扫一遍文章的开头和自标题，大致看上去可以分为两个部分：概念和机制代码。概念上主要会讲述张量Tensor、数据布局Layout、自动微分Autograd。机制代码上主要讲述算子的调用、编写新算子和成熟的贡献代码工作流。那么，

- 作为一个工程师从业者，我想要了解：

  1. Tensor的数据结构是如何设计的？为什么要这样设计？
  2. Pytorch内置支持哪些数据布局？
  3. 自动微分在工程上是如何实现的？
  4. 从Python层的Pytorch代码到底层算子调用中整个算子调用链是怎样的？
  5. 编写新算子的标准化流程是怎样的？
  6. 为Pytorch开源仓库贡献代码的标准流程是怎样的？
- 工作实践中遇到的问题：

  7. 能否自定义Tensor数据布局？有没有方便的标准化方式？
  8. 有时出于调试的需求，能否同时执行多条分支调用链？比如对于一个自定义算子，我想比较我写的算子和标准算子之间有无精度差异，能否同时自动调用二者进行比较？还是需要手动切换算子？
  9. 编写新算子时，注册新算子的native function表语法令人比较迷惑，是否能讲解？
- 假设我是一个对Pytorch了解不多的新人，我可能还想要了解：

  10. 什么是张量Tensor？为什么需要Tensor？
  11. 为什么需要多种数据布局？
  12. 自动微分在数学上的原理？
  13. 为什么一个算子可能要有多种调用链，而不是统一的实现方式？

### 我的直觉

1. Tensor的数据结构是如何设计的？为什么要这样设计？

对于一个相对比较复杂的数据容器，直观上的想法是需要一些元数据和实际数据进行分离，就像是C++ 标准库里对数据容器的设计那样。这样的设计可以使得对于数据的检索和不涉及数据底层的操作更为迅速且安全。

2. Pytorch内置支持哪些数据布局？

我已知的数据布局应该只有基于offset和stride的连续或非连续布局。不知道还有没有其他内置布局。

3. 自动微分在工程上是如何实现的？

对于每一个开启自动微分tensor，应该会有记录上一次计算操作的反向梯度传播到计算输入的tensor。通过链式一直向上传播到没有记录的tensor为止。

4. 从Python层的Pytorch代码到底层算子调用中整个算子调用链是怎样的？

直觉上，对于Python上的算子操作：

- 首先需要通过Python与C++之间的binding绑定，将操作映射到C++；
- 其次由于Pytorch需要支持不同的加速器设备，所以还需要根据算子的输入tensor所处的设备来走到不同设备的算子；
- 最后，还需要根据tensor其他属性进行调度，比如稀疏、复数、数据排布，从而到达最后的目标算子。

5. 编写新算子的标准化流程是怎样的？

在我的工作中，编写新算子主要分为两部分：

- 在自定义的高性能算子库中，使用自研AI加速芯片的类似C++的DSL进行编写运行在加速芯片上的算子代码。这部分并不在Pytorch中。
- 然后在Pytorch中添加调用算子的代码。而添加调用代码的过程也可以分为两个步骤。
  1. 先根据算子的功能与性质，实现C++的算子调用代码。
     1. 检查输入参数的数据类型、tensor形状、数据排布等属性符合预期。
     2. 然后进行调用算子库中的算子。
     3. 最后添加检查对比算子结果的步骤，以便检查算子精度问题。
  2. 然后需要在native_functions.yaml中注册算子，写明输入和输出参数。
     如上就是基本流程。

6. 为Pytorch开源仓库贡献代码的标准流程是怎样的？

猜测可能与其他GitHub开源项目类似。

- 先fork开源仓库到自己的分支。
- 然后进行修改后测试功能与CI-CD可靠性。
- 最后根据贡献文档要求规范提交PR。

7. 能否自定义Tensor数据布局？有没有方便的标准化方式？

我目前不了解Pytorch中是否存在直接定义数据布局的办法。在我们的自定义数据布局的工作中，只能采用一种提醒警告式的方式告知用户需要某些布局，并提供布局转换的算子函数，但在我们的补丁版Pytorch中实际上并无对布局变换的记录。

8. 有时出于调试的需求，能否同时执行多条分支调用链？比如对于一个自定义算子，我想比较我写的算子和标准算子之间有无精度差异，能否同时自动调用二者进行比较？还是需要手动切换算子？

对于这个问题，在我的工作经验中是直接将输入参数传输到CPU上进行重新计算。进行比较二者算子的输出结果。但不清楚是否有自动的办法。

9. 编写新算子时，注册新算子的native function表语法令人比较迷惑，是否能讲解？

注册算子的native_functions.yaml中有许多细节语法：比如感叹号!表示原地操作，函数下划线_表示会修改输入Tensor参数之类的小细节。很容易令人忘记。再添加dispatch的一些语法就更迷惑了。其中README文档虽有解释，但依旧不足够清晰。常常的做法是寻找一个类似的已经注册的算子进行照葫芦画瓢地注册。希望能有更多详细解释。

10. 什么是张量Tensor？为什么需要Tensor？

相比于标量、向量、矩阵，我们可以将张量Tensor理解为更一般的量，是更通用的数据容器。

- 标量是0阶的，只有一个数量，例如数字5；
- 向量是1阶的，可以有多个数量，但只能在一个轴上有量。例如[1,2,3]；
- 矩阵是2阶的，同样有多个数量，不同在于可以有行和列两个轴上有量。例如[[1,2],[3,4]]；
- 而张量就是根据以上的规律进行推广，可以是任意阶的，可以在任意方向轴上有量。即：[[[...]]]

张量的产生在工程中可以理解为是现实案例的需求。比如对于图像的表示，基本的方法就是为每一个像素赋予三种颜色通道RGB的数值。那么一张高为H、宽为W的图片就需要用维度形状为[H,W,3]的三阶张量进行表示。假如我有N张图片，那么就需要维度形状为[N,H,W,3]的四阶张量进行表示。以前的向量和矩阵是没办法完全表示这类需求的。所以可以表示更高阶的张量是很有必要的。

11. 为什么需要多种数据布局？

多种数据布局和自定义Tensor数据布局是很有意义的。在我的经验中，Tensor数据布局会在一些情况下显著影响后续算子的执行效率，很多时候影响算子执行效率的不一定是计算能力本身，而是对数据的访存方式。尤其是对于数据访问存在诸多硬件限制、效率不高的加速芯片。

12. 自动微分在数学上的原理？

自动微分在数学上的核心原理是链式求导法则。AI模型往往是一连串大量函数计算的堆叠。例如对于如下的从输入x到输出y的一系列函数变换

$$
u = f(x), \quad v = g(u), \quad y = h(v)
$$

那么整体函数是

$$
y = h(g(f(x)))
$$

根据链式法则：

$$
\frac{dy}{dx}
=
\frac{dy}{dv}
\frac{dv}{du}
\frac{du}{dx}
$$

PyTorch 自动做的，就是记录这些中间操作，然后在 `.backward()` 时从输出往输入方向，把这些局部导数一层层乘回去。

而对于向量、矩阵和张量的计算则会复杂一点，需要涉及到雅可比矩阵。后续有机会在单开一帖讨论吧。

13. 为什么一个算子可能要有多种调用链，而不是统一的实现方式？

这是因为对于不同的底层计算硬件，执行计算的代码和思路是完全不同的。对于CPU上，我们可能会使用一些单指令多数据（SIMD）思路的高性能指令集进行计算，比如AVX512；对于GPU，我们基于单指令多线程（SIMT）思路使用CUDA编程语言；而对于更多其他种类芯片，比如华为的NPU、谷歌的TPU等等多种多样的计算芯片，各自的算子计算逻辑又可能不一样。几乎不可能在底层统一进行实现。
不过话又说回来，随着triton、tilelang等高层次并行编程语言的发展，借助强大的编译器，在相对高层上统一实现代码是有可能的，但已经不属于本文Pytorch主题范畴。也挖一坑，以后可以单开一贴讨论。

## 学习过程

本篇博客主要为那些想要参与Pytorch工程开发，为Pytorch开源项目贡献代码的人所讲述Pytorch的基本概念与机制。作者将内容分为了两部分：概念与机制。其中概念主要讲述张量Tensor与自动微分，而机制部分主要讲述代码逻辑和贡献代码的流程。由于内容较多，我在这里将其进一步细化为五个主题部分：张量Tensor、自动微分Autograd、基本代码结构、编写算子以及高效的工作流。其中前两部分属于原文的概念部分，后三部分属于机制部分。

### 1. 张量Tensor

在张量主题中，主要讲述了Tensor的基本概念、Tensor的步长表示法、基于Tensor属性的算子调度和关于Tensor的Pytorch扩展。

##### 1.1 Tensor的基本概念

作者直接给出了在Pytorch中张量Tensor的基本概念就是一个任意阶任意维的存储数据的结构，可以理解为向量、矩阵的更高阶推广。

那么对于某一个特定的Tensor，他就有着一些属性用于表示他的特点。就像人有身高体重之类属性来表示人的特点。

那么Tensor有哪些属性呢？从数学角度可以自然地想到，Tensor的**阶数**、**维度**肯定是他的属性。
例如对于这样一个tensor

```text
[
    [
        [0, 8, 9],
        [6, 0, 4],
        [9, 7, 8]
    ],
    [
        [0, 3, 1],
        [4, 1, 3],
        [0, 3, 5]
    ],
    [
        [3, 5, 3],
        [9, 0, 1],
        [4, 2, 2]
    ]
]
```

这就是一个阶数为3的、维度为(3, 3, 3)的Tensor。有时，还会称这个(3, 3, 3)为**sizes尺寸**或**shape形状**。

以上就是从理论出发的Tensor基本概念。而为了从数学理论落地到计算实践，Tensor需要加上更多限制，同时也就带来更多属性。

1. dtype（数据类型Data Type）：在计算机的有限空间中，我们无法完全精准无误地表示拥有无限位数的实数。于是就诞生了使用有限位数表示数字的各种数据类型。学习过基本编程课程的同学应该已经知道一些数据类型，例如：int、long、float、double。而在Pytorch和深度学习领域，数据类型的位数是十分重要的，因为这代表了这一种数据类型能够表示的数值范围和精度。于是，我们常称以上常见数据类型为int32、int64、float32和float64。此外，在深度学习领域，模型常常不对精度特别敏感，拥有一定的容错，这就引发了大量对低精度计算的探索研究，比如int8、int4、fp8、fp4。未来有机会的话，这也是一个值得一讲的主题。
2. device（计算设备）：在深度学习领域，与Tensor相关的计算操作往往都是可以并行化的，比如张量相加、相乘和矩阵乘等运算操作。而对于并行计算，GPU、NPU、TPU、LPU等等各种加速芯片设备的计算效率远高于常规CPU。于是，Pytorch常常会借助这些加速计算的设备实现快速的计算。而此时，这个张量存储在哪个计算设备上就十分重要。只有将张量存储到指定设备上才能调用这个设备的计算能力进行加速。
3. stride（步长）/layout（数据布局）：这两个属性的引入被作者称为Pytorch的特性之一。后面一节我们会详细讲述。

以上就是Tensor常用到的基本属性。实际应用中为了兼容更多场景，还会有更多属性，后续我们遇到了再进行讲述。描述Tensor特点的这些属性数据被称为“元数据”，这是由于Tensor本身内部即存储了大量数据，从而与其内部数据相对应。

##### 1.2 Strided Representation（步长表示）

在上一节中我们引入了stride，他是Tensor的一个属性，但并未详细讲述他。那么在本节中，我们就将进一步介绍步长的概念。

首先，stride步长是什么？在原文中并未给出明确的定义，而是通过描述步长的功能来给出对步长的直觉。如下：

> Suppose that I want to access the element at position tensor[1, 0] in my logical representation. How do I translate this logical position into a location in physical memory? Strides tell me how to do this: to find out where any element for a tensor lives, I multiply each index with the respective stride for that dimension, and sum them all together.

译：假设我想要获取访问在tensor的[1, 0]逻辑位置的元素。我该如何将这个逻辑位置转为物理内存上的位置？步长可以告诉我如何去做到这一点：要找出张量中任意元素的位置，我可以将每个索引与该维度对应的步长相乘，然后将所有结果相加。

我认为关于stride这一点上，原文的讲述是相对模糊的。我认为可以参考[Pytorch官方文档](https://docs.pytorch.org/docs/2.12/generated/torch.Tensor.stride.html)中的描述

> Stride is the jump necessary to go from one element to the next one in the specified dimension dim.

译：Stride是沿着某一特定维度，从一个元素到下一个元素所必需跳过的元素个数。

举个简单的例子，假设有这样一个数据类型为int32，维度为(2, 2)且按最后一个维度轴连续存储在内存中的2阶Tensor，称之为A。那么逻辑上就可以表示为：

```text
A = [
    [2, 8],
    [6, 0]
]
```

同时，假设物理内存上的情况可以表示为：

| 内存地址 | 内存数据 |
| :------: | -------- |
|    0    | 2        |
|    4    | 8        |
|    8    | 6        |
|    12    | 0        |

其中， $A[0,0]=2,A[0,1]=8,A[1,0]=6,A[1,1]=0$，且每经过一个元素内存地址增加了4是因为每个int32数据类型的数据需要占用4个字节的内存空间。
那么，沿着第1个维度轴从一个元素到下一个对应元素，比如从A[0,0]到A[1,0], 所需要跨越的元素个数就是2个，stride就是2。
而沿着第2个维度轴，从一个元素到下一个对应元素，比如从A[0,0]到A[0,1]，所需要跨越的元素个数就是1个，stride就是1。
于是综合两个维度，这个Tensor的stride就是(2,1)。

那么，有的小伙伴就会有疑问了：原文中提到的概念是对于张量中任意元素的位置，可以将每个索引与该维度对应的步长相乘，然后将所有结果相加。这是说的元素在物理内存中的位置与步长之间的关系。但我们刚才看到的stride的定义是元素之间的物理内存上的距离。这好像不太一样诶！

确实不一样，但我们可以通过相对位置计算得到绝对位置，二者是互通的。假设张量中第1个元素的内存地址为0，那么第n个元素与第1个元素之间的相对距离就是第n个元素在物理内存的绝对位置地址。

比如依旧考虑先前例子中的Tensor A：对于A[1,0]元素，与A[0,0]之间的元素个数距离是2，而根据索引和步长的对应相乘计算可以得到

$$
1 \times 2 + 0 \times 1 = 2
$$

可以发现，二者是相等的。所以，我认为实际上这计算绝对位置的方法应该属于stride的性质。说到这，stride的基本概念应该大致清晰了。

然后，我们就来到了为什么需要stride？为什么不把直接的内存地址偏移量作为所谓的stride呢？

这是为了方便进行访问读取数据。拥有基本C/C++编程知识的同学应该了解：对于数组、链表、堆栈等数据结构的访问，我们常常都是通过指针地址进行访问的。在Pytorch中，也是如此。
当我们编写算子处理Tensor计算时，我们往往是以Tensor的首元素的地址作为输入参数的。此时，stride就可以告诉我们如何从首元素的地址指针出发，加上stride作为偏移量，访问到Tensor中任意元素的地址，从而进行数据的访问读取。

为什么不直接把内存地址偏移量作为所谓的stride呢？这是因为指针本身就带有数据类型的属性，指针加上一个整数就会自动乘以数据类型的字节数进行偏移计算了。比如对于int32类型的数据，每个元素占用4个字节，那么指针加上1就会自动乘以4进行偏移计算了。所以我们不需要再把内存地址偏移量作为所谓的stride了。

进而，有了stride，我们可以实现一些特别功能。
比如说对于一个先前例子中的Tensor A，如果我想要获取这个Tensor的第二行，也就是A[1,:]，那么我就可以通过stride来实现。由于A[1,0]的索引是(1,0)，对应的步长是(2,1)，所以A[1,0]元素在物理内存中的位置就是

$$
1 \times 2 + 0 \times 1 = 2
$$

也就是A[1,0]元素的内存地址是首元素地址加上2个元素的偏移量。由于A[1,1]元素的索引是(1,1)，对应的步长也是(2,1)，所以A[1,1]元素在物理内存中的位置就是

$$
1 \times 2 + 1 \times 1 = 3
$$

也就是A[1,1]元素的内存地址是首元素地址加上3个元素的偏移量。于是，我们就可以通过stride来访问到A[1,0]和A[1,1]元素的内存地址，从而获取到第二行的数据了。

不过，顺带一提，我们也可以通过offset，也就是整体Tensor的地址偏移量，来实现这个功能。由于A[1,0]元素在物理内存中的位置是首元素地址加上2个元素的偏移量，而A[1,1]元素在物理内存中的位置是首元素地址加上3个元素的偏移量，所以这些数据也是连续的，我们也可以通过offset来访问到A[1,0]和A[1,1]元素的内存地址，从而获取到第二行的数据了。

再举一个例子，那么当想要获取这个Tensor的第一列，也就是A[:,0]，那么我们就可以通过stride来实现。由于A[0,0]的索引是(0,0)，对应的步长是(2,1)，所以A[0,0]元素在物理内存中的位置就是

$$
0 \times 2 + 0 \times 1 = 0
$$

也就是A[0,0]元素的内存地址是首元素地址加上0个元素的偏移量。由于A[1,0]元素的索引是(1,0)，对应的步长也是(2,1)，所以A[1,0]元素在物理内存中的位置就是

$$
1 \times 2 + 0 \times 1 = 2
$$

也就是A[1,0]元素的内存地址是首元素地址加上2个元素的偏移量。于是，我们就可以通过stride来访问到A[0,0]和A[1,0]元素的内存地址，从而获取到第一列的数据了。

我们可以通过改变Tensor的stride来实现不同的数据访问方式，从而在进行切片、形状改变等一系列操作时，不进行实际的数据复制，而是通过改变stride来实现数据的访问方式的改变，从而实现高效的计算。
例如对于如下代码

```python
import torch
A = torch.tensor([
    [2, 8],
    [6, 0]
])
B = A[:,1]
```

在这个代码中，我们通过切片操作获取了A的第一列数据，并将其赋值给了B。B和A共享了同一块内存空间。值得一提的是，如果后续B的数据发生了改变，那么A的数据也会发生改变。
如果我不想A的数据也发生改变，那么我就需要进行数据复制了。比如可以通过如下代码实现：

```python
import torch
A = torch.tensor([
    [2, 8],
    [6, 0]
])
B = A[:,1].clone()
```

基于Stride的表示方法可以实现各种有趣的视图功能。文中还给出了一个有趣的可视化工具可以让我们看到在各种参数作用下，Tensor实际表示的内存布局情况：https://ezyang.github.io/stride-visualizer/index.html

最后，Pytorch中如何为Tensor实现stride呢？
既然底层数据需要保持不变，而只改变上层的访问方式。那么我们就需要将底层“存储”和上层“张量”进行分离了。Pytorch中就是通过Tensor与Storage的分离来实现的。Tensor中存储了Tensor的元数据属性，而Storage中存储了Tensor的数据内容与底层的元数据。通过这种分离，我们就可以在不改变底层数据内容的情况下，通过改变Tensor中的stride等属性来实现不同的数据访问方式了。
任何Tensor，无论简单连续的还是复杂变换过的，都是基于Tensor-Storage分离的设计实现的。Tensor中的stride属性就是通过这种设计实现的。

文中还提到了一点，团队正逐渐想让Storage不再成为独立概念，而是也是作为张量的一种特殊视图来实现的。也就是说，未来可能会将Storage也作为Tensor的一种特殊视图来实现，而不再是一个独立的概念了。不知道现在是否已经实现了。后续有机会的话可以看看如今的源码单开一贴来讲讲Storage的设计演变。

#### 1.3 基于Tensor属性的算子调度

在前两节里，我们已经知道一个 Tensor 身上带有 device、dtype、layout 这些属性（外加上一节细讲的 stride）。那么很自然就冒出一个问题：当我写下一行 `torch.add(a, b)`，PyTorch 到底是怎么**根据这些属性，找到那段真正该执行的算子代码**的？

其实在「先猜再学」里我已经猜过这条调用链：先经过 Python 到 C++ 的 binding，再按 device 走到对应设备的算子，最后按数据排布等属性走到目标算子。读完发现大方向是对的——确实存在这样一层层“按属性分流”的过程，这个过程就叫 **dispatch（调度）**。但细节上我猜得并不准，有两处理解偏差，正好记下来。

按 Ezyang 的说法，一次算子调用从外到内大致经过这么几层 dispatch。最外层是 **variable（autograd）调度**，原文说它负责 *unwrapping variables, calling the underlying implementation, and then rewrapping the results*——它不挑计算 kernel，而是为后续的反向传播做准备；具体准备什么，我们留到 §2 自动微分 再展开，这里只要记住它在最外面。再往里是 **device 加 layout 的调度**：*“The first dispatch is based on the device type and layout of a tensor: e.g., whether or not it is a CPU tensor or a CUDA tensor.”* 这一层决定走 CPU 还是 CUDA 实现、是普通 strided 还是 sparse 布局。最里面是 **dtype 调度**，原文说它 *“is just a simple switch-statement”*——float32 和 int 的乘法本就是两份代码，靠一个 switch 选到对应那份。

第一处误解，是我把上一节的“连续性”概念误用到了这里，以为 layout 调度是按“连续 vs 非连续”来分的。其实不是。这里的 layout 指的是 `Layout` 这个枚举——Strided（普通 dense）、Sparse、Mkldnn 这种**整体布局类型**，与连续性无关。一个连续的 dense tensor，和一个转置后非连续的 view，它俩的 layout 都是 Strided，**会 dispatch 到同一个 kernel**。那连续性在哪里处理？在 kernel **内部**：element-wise 算子默认走 TensorIterator，直接按 stride 读非连续数据（通常还带一条 contiguous 的快路径）；而 matmul、conv 这类要进 BLAS/cuDNN 的，则可能先 `.contiguous()` 再算。也就是说，连续性是 dispatch **之后**的事，不参与选 kernel。

第二处误解，是我以为 requires_grad 这层调度是**最后**才做的——直觉上 grad 像一个事后的附加步骤。其实它在**最外层**、最先做。一个便于理解的角度是：先有了带 device/dtype/layout 的普通 tensor，再在它外面套一层 variable 来实现 autograd；既然是套在最外面的一层，那么往里走时它自然最先被剥开。

由此还引出一个更基础的问题：device/layout/dtype 我都能理解成“选不同的 kernel 实现”，但 variable 这一层在“选”什么？答案是——**它并不在选 kernel，而是在做记录，为反向传播做准备**。这就引出这一节最反直觉、也最关键的一点：**dispatch 不只是“选计算 kernel”，它是一套可叠加的“拦截层”机制——每一层都在算子前后插入一段行为，而只有最里面那层才是真正执行计算的 kernel。** autograd 是最典型的一层，此外 autocast、`torch.func` 的 vmap/grad、functionalization 也都是挂在 dispatch 上的拦截层。把心智模型从「dispatch = 选 kernel」修正为「dispatch = 一组依次嵌套的拦截层，最内层才是 kernel」，这一节就理顺了。

最后补一个把上面串起来的结构细节：device 和 layout 实际上是**合成一个 backend key**（CPU、CUDA、SparseCUDA……）一起 dispatch 的，并不是两次独立分流；而 dtype 并不是 dispatcher 级别的 key，它是落在 kernel **内部**的那个 switch。所以更准确的图景是：variable（最外）→ backend = device × layout（一层）→ kernel 内的 dtype switch（最内）。想对照源码看的话，dispatch key 的定义在 `c10/core/DispatchKey.h`，dtype 的 switch 就是 `aten/src/ATen/Dispatch.h` 里的 `AT_DISPATCH_*` 宏。

这也顺带回答了我在「先猜」里提出的疑问：为什么一个 add 要准备这么多份 kernel？因为 device × layout × dtype 本身就是一个**笛卡尔积**——原文说得很直接，*“in principle the combination could make sense, and thus we support expressing it.”* 各种硬件、布局、数据类型的组合，原则上每一种都可能需要一份特定实现，数量自然就多了。

还有一点这里先不展开：现代 PyTorch 里 `Variable` 和 `Tensor` 已经合并，所谓“剥开 variable”在实现上是 redispatch 时把 autograd key 排除掉——这个机制，以及 variable 层究竟记录了什么，都留到 §2 自动微分。

#### 1.4 关于Tensor的Pytorch扩展

上一节我们看到，一次算子调用是按 device、layout、dtype 这几个属性层层 dispatch、最终落到某段具体 kernel 的。那么一个很自然的问题就接着冒出来了：如果现有的 device、layout、dtype 都不够用，我想往 PyTorch 里加一种"新的 Tensor"，该怎么加？ 这一节讲的就是扩展 Tensor 的几种方式。对我而言这一节格外切身——我日常做的自研后端适配，本质上就是这里说的"扩展"之一。

先把框架立起来。Ezyang 指出，device、layout、dtype 这三者唯一确定了一个 tensor 是什么，原文说它们的笛卡尔积定义了所有可能的张量："The Cartesian product of these parameters define all of the possible tensors you can make." 这三者各管一件事：device 描述张量的物理内存实际存在哪里，layout 描述我们如何在逻辑上解释这块物理内存，dtype 描述每个元素里到底存的是什么。

理解了"笛卡尔积"这个框架，就能看出沿三条轴扩展的成本是极不对称的。沿 layout 或 dtype 扩展往往是"局部"的：我新增一种 layout，可能只是为某个特定算子的特殊需求服务，不必让全量算子都支持它；我新增一种 dtype，也只是在 kernel 内部那个 AT_DISPATCH_* 的 switch 里多一个分支。但沿 device 扩展——也就是我做的事——是"全局"的：我欠下的是整张笛卡尔积的一整列，原则上每一个算子、配上每一种 layout 和 dtype，都要有一份对应的 kernel 才算完整。而且代价还不止算子：一个新设备要真正可用，还得把 graph 捕获、profiler、通信、内存分配、stream 这些运行时能力一并适配过去。这也是为什么 PyTorch 2.12 引入设备无关的图捕获 torch.accelerator.Graph 对我们这些后端开发者是刚需——它把"每个新后端都重写一遍图捕获"这件重复劳动抽象掉了。

不过，"想加点新东西"并不等于"非得做这种重量级扩展"。Ezyang 给了一个很关键的判据来决定该走哪条路：看你是否需要让这个张量在 autograd 的反向传播过程中被一路传递下去，原文是 "whether or not you need to pass this tensor along during the autograd backwards pass." 这个判据为什么是 autograd？回到 §1.3 的整体逻辑就清楚了：autograd 是挂在最外层的那层拦截，而它只认识 Tensor。如果我只是用一个普通的 Python wrapper 类把张量包起来，那么这个壳对 autograd 是不可见的，梯度链一遇到它就断了。于是就分出了三条路：

| 需求                                                  | 手段                     | 是否需要在源码仓库中修改 |
| ----------------------------------------------------- | ------------------------ | ------------------------ |
| 只是个新对象，不需要梯度穿过它                        | wrapper 包装类           | 可完全 out-of-tree       |
| 需要一个可导的新算子（如 STE）                        | 自定义 autograd.Function | 可 out-of-tree           |
| 新对象要作为 tensor 本身参与全套 dispatch 与 autograd | 真正的 Tensor 扩展       | 传统上需 in-tree         |

把这三条路对到具体的最佳实践上，理解会更牢。PackedSequence（打包变长序列那个对象）是 wrapper 的典范：它内部就是一个普通张量 data 加上 batch_sizes 之类的元数据，梯度是穿过 data 这个普通张量流动的，那个外壳本身从不需要进入 autograd——所以它做成 wrapper 完全够用。反过来，稀疏张量就必须是真扩展：一个稀疏张量的梯度本身也是稀疏结构的，autograd 必须能构造出一个稀疏的梯度并继续往上传，你没法用一个外壳糊弄过去。复数也是同样的故事——2019 年之前大家用"最后一维等于 2"来假装复数，那本质是 wrapper 思路，可一旦要做到全算子覆盖加上 autograd，这种假装就撑不住了，于是复数最终被提升为真正的 complex64/128 dtype。

这里有一个很值得记下的反例：训练后量化（PTQ）用的 qint8 配 QuantizedCPU 后端，它只服务推理、根本不参与反向，可它仍然被做成了真扩展。这说明 autograd 判据只是"需要真扩展"的充分条件，而不是唯一条件。量化之所以做真扩展，买的是另外两样东西：一是透明的 dispatch，让 conv2d、matmul 照常写出来就能被 dispatcher 自动路由到 FBGEMM、QNNPACK 那些整数专用 kernel，而不必在 Python 里手动拦截整个算子面；二是真正的低比特存储，让 storage 实际就是 int8 字节，省下四倍内存、并让 kernel 直接读原始 int8。

理解了这套判断标准，我正好可以回看自己工作里的一次取舍。我们曾经为了让数据布局对硬件计算更友好，做了一套自定义的布局转换：自定义了布局转换的算子，也自定义了基于这种特殊布局的计算算子。现在用这张表来对照，这套实现其实落在"自定义算子"那条路上——是 op 级的。但问题在于，转换之后的张量是还要继续参与训练的，autograd 必须理解这个布局，所以它本应落在真正的 layout 扩展上。这方面最贴切的先例是 Mkldnn（oneDNN 的 blocked/packed 布局）：它同样是为硬件友好而做的分块排布，被实现成一个真正带 layout 的一等张量，并且参与 autograd——和我们的场景几乎一一对应。当然，还要先分清需求的轻重：如果我的布局只是 stride 的重排（数据还是连续的 strided，只是轴的顺序变了），那连 layout 扩展都不需要，用 memory_format（channels_last 那一套）就够了；只有当它是真正不同的分块打包时，才需要上升到真正的 Layout 扩展。我们当初那套 op 级方案的局限，也正好被这张表照了出来：因为采用的是"提醒式告知 + 布局转换算子、但补丁版 PyTorch 并不记录布局变换"的做法，这个布局对 PyTorch 而言始终是"账外"的——autograd、.contiguous()、view 操作、序列化、各种通用算子都不知道这些张量带着特殊布局，于是每一条路径我们都得手动去拦。而真扩展（或退一步的 memory_format）的价值，恰恰是把"这个张量是什么布局、它的梯度又对应什么布局"集中登记一次，让全栈自动认得它。

最后留两个坑。其一，本节讲的"真扩展传统上要 in-tree"是 2019 年的图景；2021 年之后 PyTorch 提供了 __torch_dispatch__ 的 Tensor 子类——它本身就是一个 Tensor，因此 autograd 认得它，却又能完全 out-of-tree 开发，正好填上了"既要 autograd、又不想动源码"的那个空档，torchao 的量化张量、NF4、DTensor 都走这条路。这对做后端的人是比硬塞一个 dispatch key 更轻的姿势，值得后续单开一篇细看。其二，是 §1.2 留下的那个坑：Storage 是否已经被"降格"成 Tensor 的一种特殊视图，也一并留待看源码时再追。

铺垫到这里，扩展 Tensor 的几条路就清楚了。而这几层里最特殊的，始终是挂在最外面的那层 variable（autograd）——它不挑 kernel，只做记录。它到底记录了什么、又是怎么把反向图建起来的，正是 §1.3 和这一节反复欠下、却一直没还的那笔债。下一节，我们就正式走进自动微分。

### 2. 自动微分Autograd

在自动微分主题中，我们先用一节数学预备（§2.0）从导数铺到矩阵求导，再分四节展开：Variable 到底记录了什么（§2.1，grad_fn、saved tensors 与反向图）、为什么自动微分采用反向模式（§2.2）、autograd 在工程上如何挂在 dispatch 机制之上（§2.3），以及 saved tensors 带来的显存代价与权衡（§2.4）。

#### 2.0 数学预备：从导数到矩阵求导

在正式拆解 autograd 之前，我想先单开一节补数学。原因后面会看清——autograd 的工程实现几乎是一套数学的**逐字翻译**，$\text{grad\_input} = \text{grad\_output} \cdot J_\text{local}$ 这一个式子会贯穿始终。把背后的数学（链式法则、梯度、雅可比、矩阵求导）先理顺，2.1 和 2.2 就能轻装上阵。这一节对刚入门的读者是地基，对熟手是一张复习整图；已经烂熟的同学可以直接跳到 2.1。

我用一条主线把它串起来：**微分 $df = (\text{导数}) \cdot dx$**——而那个"导数"，会从一元的斜率，一步步推广成梯度、雅可比、矩阵导数。

**目的：我们到底要算什么。** 训练就是用梯度下降最小化一个**标量** loss $L$，参数按这条式子一步步更新：

$$
\theta \leftarrow \theta - \text{lr} \cdot \frac{\partial L}{\partial \theta}
$$

这里 $\theta$ 是模型参数（权重），$\partial L/\partial\theta$ 是 loss 对参数的导数——它刻画"参数往某方向动一点、loss 会怎么变"，方向上指向 loss **上升**最快的那边。所以在前面**减去**它，就是让参数朝 loss **下降**的方向挪一步；$\text{lr}$（学习率）控制这一步迈多大；箭头 $\leftarrow$ 表示这是一次次反复迭代的赋值更新。整个训练，无非是不断重复这个动作、把 loss 一点点推低。可见**核心诉求只有一句——求 $L$ 对所有参数 $\theta$ 的偏导**。这里再立一个贯穿全文的约定：**梯度与参数同形**（既然要拿梯度去和参数相减，两者形状必须一致）。

**① 一元微分：导数是"局部线性近似的斜率"。** 对 $f:\mathbb{R}\to\mathbb{R}$，导数 $f'(x)$ 的本质，是在 $x$ 处用一条直线近似曲线：

$$
df = f'(x)\,dx
$$

即"输入动一点 $dx$，输出大约动 $f'(x)\cdot dx$"。再加上链式法则 $(f\circ g)'(x) = f'(g(x))\cdot g'(x)$，整套自动微分要做的，就是把这两件事推广到多输入、多输出、矩阵参数。

**② 多元、单输出：梯度。** 对 $f:\mathbb{R}^n\to\mathbb{R}$（多输入、输出仍是标量，正是 loss 的形状），先有**偏导** $\partial f/\partial x_i$（只动第 $i$ 个输入时的斜率），再把所有偏导排成一个**与输入同形**的向量，就是**梯度**：

$$
\nabla f = \left[\frac{\partial f}{\partial x_1},\dots,\frac{\partial f}{\partial x_n}\right]
$$

它指向函数上升最快的方向（所以梯度下降取 $-\nabla f$）。多元版的 $df = (\text{导数})\cdot dx$ 写作全微分 $df = \nabla f \cdot dx$；而 $\nabla f \cdot v$ 是沿方向 $v$ 的变化率，叫方向导数。

**③ 多元、多输出：雅可比矩阵。** 对 $f:\mathbb{R}^n\to\mathbb{R}^m$（多输入**且**多输出，比如网络中间一层），"导数"升级成**雅可比矩阵** $J\in\mathbb{R}^{m\times n}$——它把每个输出对每个输入的偏导排成一张表，第 $i$ 行第 $j$ 列是 $J_{ij} = \partial f_i/\partial x_j$，完整写出来就是：

$$
J = \begin{bmatrix} \dfrac{\partial f_1}{\partial x_1} & \dfrac{\partial f_1}{\partial x_2} & \cdots & \dfrac{\partial f_1}{\partial x_n} \\ \dfrac{\partial f_2}{\partial x_1} & \dfrac{\partial f_2}{\partial x_2} & \cdots & \dfrac{\partial f_2}{\partial x_n} \\ \vdots & \vdots & \ddots & \vdots \\ \dfrac{\partial f_m}{\partial x_1} & \dfrac{\partial f_m}{\partial x_2} & \cdots & \dfrac{\partial f_m}{\partial x_n} \end{bmatrix}
$$

它同样满足 $df = J\,dx$（多输出版的 $df = (\text{导数})\cdot dx$）。

雅可比的第 $i$ 行就是第 $i$ 个输出的梯度。可见**梯度是雅可比在 $m=1$ 时的特例**（退化成 $1\times n$ 行向量）。而链式法则在这里有了**矩阵形式**——若 $x \xrightarrow{f} h \xrightarrow{g} y$，则

$$
J_{g\circ f} = J_g \cdot J_f
$$

一句话：**链式法则 = 雅可比连乘**。多层网络就是 $J = J_L \cdot J_{L-1} \cdots J_1$。

把一个网络一直接到标量 loss，就得到 $\nabla L^\top = J_L \cdot J_{L-1} \cdots J_1$（形状 $1\times n$）。这里藏着一个关键问题：这串连乘，**先乘哪一对**？这正是区分"正向 / 反向传播"的分水岭——我们留到 §2.2 专门展开，这一节先只把数学工具备齐。

**④ 矩阵求导：当参数是一整个矩阵。** 实战里参数 $W$ 往往是矩阵（如线性层）。直接对矩阵求导，需要两件工具。其一是**约定**：标量对矩阵的导数 $\partial L/\partial W$ 与 $W$ 同形（这样才能逐元素相减）。其二是**微分迹法**——任何标量 $L$ 的微分都能整理成 $dL = \mathrm{tr}\!\left((\partial L/\partial W)^\top dW\right)$ 的样子，所以只要把 $dL$ 化简成 $\mathrm{tr}(M\cdot dW)$（$M$ 为某个矩阵），那个矩阵转置就是梯度，绕开逐元素求导的泥潭。几个常用结论（新读者记结论即可）：

| 前向               | 导数 / 梯度                                                                                                           |
| ------------------ | --------------------------------------------------------------------------------------------------------------------- |
| $L = a^\top x$   | $\partial L/\partial x = a$                                                                                         |
| $y = Wx$         | $J = W$                                                                                                             |
| $L = x^\top A x$ | $\partial L/\partial x = (A+A^\top)x$                                                                               |
| $Y = XW$         | $\partial L/\partial X = G\cdot W^\top$，$\partial L/\partial W = X^\top\cdot G$（$G = \partial L/\partial Y$） |

最后一行就是**线性层的 backward**：用迹法验证，$dL = \mathrm{tr}\!\left(G^\top(dX\cdot W + X\cdot dW)\right) = \mathrm{tr}(WG^\top dX) + \mathrm{tr}(G^\top X\,dW)$，两项分别读出 $\partial L/\partial X = GW^\top$、$\partial L/\partial W = X^\top G$。这条恒等式，我们在 §2.1、§2.2 会反复用到。

**小结：一个公式贯穿始终。** 从一元的斜率到矩阵求导，变的只是"导数"的形态——数 → 向量（梯度）→ 矩阵（雅可比）→ 结构化矩阵运算，而 $df = (\text{导数}) \cdot dx$、以及"链式法则 = 导数连乘"这两条主干始终不变。反向传播，无非是这条连乘从标量 loss 那头起手算起。

> **给新读者的最小集**：只需扛走四件事——① 链式法则；② 梯度 = 偏导组成、与参数同形、指最速上升；③ 雅可比 = 多输出版的导数，链式法则 = 雅可比连乘；④ 反向传播 = 从标量 loss 端起手的连乘。
> **给复习者的锚点**：微分迹法 $dL = \mathrm{tr}(G^\top dW)$ 读梯度 + 上面那张恒等式表 + 一句"save 集合 ≡ $J_\text{local}$ 的依赖项"。

#### 2.1 Variable 记录了什么：grad_fn、saved tensors 与反向图

如果说前面讲的张量让 PyTorch 看起来还只是一个"带设备的 Numpy"，那么真正把它和 Numpy 区分开的，是自动微分（autograd）。Ezyang 说得很直接："The distinguishing characteristic of PyTorch when it was originally released was that it provided automatic differentiation on tensors."而在 §1.3、§1.4 里我们反复欠下一笔债——dispatch 最外层那层 variable，"不挑 kernel、只做记录"，可它到底记录了什么？这一节就把它还上。

先定个性：autograd 实现的是**反向模式自动微分（reverse-mode）**——前向把一连串算子正着算一遍，反向时再把这条计算链"倒着走一遍"，沿途把局部导数乘起来，原文叫 "we effectively walk the forward computations backward to compute the gradients."至于为什么是"反向"走而不是"正向"走，留到 §2.2 专门讲，这里先接受这个设定。

要支持"倒着走一遍"，前向时就得多存一些信息。Ezyang 把张量的数据结构做了调整：原本张量只指向一块 storage，现在外面再包一层 variable，额外存一份 **AutogradMeta**——"a variable which wraps this tensor, and also stores more information (AutogradMeta), which is needed for performing autograd when a user calls loss.backward()."那么这份元数据里到底记了什么？

在「先猜再学」里，我对这件事的直觉其实只对了一半：我猜"每个开启微分的 tensor 会记录上一次的操作，然后沿链一直往上传，直到没有记录的 tensor 为止"。"记录上一次操作"、"往上传到叶子为止"这两点都对，但我漏了关键的另一半——光知道"做了什么操作"还不足以算出反向，**还得把"反向时要用到的前向中间值"一并存下来**。所以 variable 层记录的是两件事：

1. **grad_fn（反向函数句柄）**：标记这个张量是被哪个算子算出来的，从而知道反向该调哪段代码。比如 `c` 由加法得到，`c.grad_fn` 就是 `AddBackward`。
2. **saved tensors（反向要用的前向张量）**：因为绝大多数算子的反向都要用到前向的某些值。$z = x \cdot y$ 的反向 $\partial z/\partial x = y$、$\partial z/\partial y = x$，要用到输入 $x$、$y$；$y = \exp(x)$（即 `x.exp()`）的反向 $\partial y/\partial x = \exp(x) = y$，要用到输出 $y$。这些值在前向时就被对应的 grad_fn 节点"存档"，一直留到反向才取用。

这里我自己踩过一个小坑，正好记下来：一开始我以为 `relu` 的反向要存"输入"（毕竟 relu 的导数看输入的符号），后来发现 PyTorch 实际存的是"输出 `y`"——因为对 relu 而言输出和输入同号，存输出一样能判断该不该让梯度通过，还能让输入缓冲早点释放。这说明"存输入还是存输出"是按"哪个够用且更省"来定的，并不是死板地存输入。

接着看这些 grad_fn 是怎么连起来的。`c.backward()` 是从 `c` 出发的，所以挂在 `c` 上的 grad_fn 必须知道"梯度算完了该送给谁"——它通过一组边（源码里叫 `next_functions`）指向它的各个输入各自的 grad_fn。于是所有 grad_fn 节点连成一张**反向图（DAG）**，方向是**从输出指回输入**。这里方向特别容易搞反：前向的数据是 `a`、`b` → `c` 地流，而反向图是 `c.grad_fn` → `a`/`b` 的 grad_fn 地连，二者正好相反。

用我们练手的例子 `y = (a * b).relu()` 串一遍（`a`、`b` 都是 `requires_grad=True` 的叶子）：前向先 `tmp = a * b`、再 `y = relu(tmp)`；反向图则是 `ReluBackward → MulBackward → AccumulateGrad(a) / AccumulateGrad(b)`。这张图我画在了同目录的 `autograd_test.drawio`，可对照着看。其中两个细节值得点出：

- 叶子张量 `a`、`b` 自己的 `grad_fn` 是 `None`（表示"我不是某个算子算出来的"），但它们在反向图里对应的节点是 **`AccumulateGrad`**——正是它把算到的梯度**累加**进 `a.grad`、`b.grad`。所以"张量的 grad_fn 属性"和"它在反向图里对应的节点"是两回事，叶子尤其要分清：属性是 None，干累加活的却是一个独立的 AccumulateGrad 节点。
- 既然是"累加"，每个训练步开始前就得 `zero_grad()` 把上一步的梯度清掉，否则梯度会一步步越加越多。

`backward()` 做的事，就是从输出节点出发、沿这张反向图按**反向拓扑序**遍历：每到一个节点，调用它的 backward、用它存档的 saved tensors 算出梯度、再顺着边把梯度送给上游节点，直到汇集到 AccumulateGrad、写进叶子的 `.grad`。

最后强调一点：这张反向图**不是预先编译好的**，而是前向每执行一个算子就顺手连一条边、即时长出来的——这就是 PyTorch 的"动态图"（define-by-run），也是它早年相对 TensorFlow 静态图最受欢迎的特性之一。

到这里，"variable 层记录什么"这笔债就还清了：**grad_fn 选反向算子、saved tensors 供反向取值、next_functions 连成反向图、AccumulateGrad 收口到叶子**。但还留着三个线头，正好引出后面三节：① 为什么自动微分要"反向"走、而不是"正向"走？（§2.2，从 vjp / 雅可比的角度）② 这套"记录"在工程上具体挂在 dispatch 的哪一层、`Variable` 和 `Tensor` 合并后所谓"剥开 variable"又是什么意思？（§2.3）③ saved tensors 一直留到反向才释放，正是训练显存的大头——它和激活重计算、in-place 修改的陷阱之间该怎么权衡？（§2.4）

#### 2.2 为什么是反向模式（reverse-mode）自动微分

§2.0 末尾我们停在一个问题上：网络到标量 loss 的雅可比连乘 $\nabla L^\top = J_L \cdot J_{L-1} \cdots J_1$，链式法则没规定**先乘哪一对**。这个看似无关紧要的结合顺序，恰恰就是"正向传播 / 反向传播"的分水岭。这一节就回答：autograd 为什么一律选**反向模式**。

**两种结合顺序，就是两种自动微分模式。**

- **右结合** $J_L(\cdots(J_1 v))$：从最靠近**输入**的 $J_1$ 起手，每步是"雅可比 × 向量"（Jacobian-vector product, Jvp）。导数**沿前向方向**（输入→输出）累积——这叫**正向模式**。
- **左结合** $((u^\top J_L)J_{L-1})\cdots$：从最靠近**输出**的 $J_L$ 起手，每步是"向量 × 雅可比"（vector-Jacobian product, vJp）。导数**逆前向方向**（输出→输入）累积——这叫**反向模式**，也就是反向传播。

**先把正向模式讲清楚——这里有个极易混淆的点。** 正向模式**不是**数值微分。数值微分是 $(f(x+h)-f(x))/h$，是近似、还受舍入误差夹击；正向模式则和反向模式一样，用的是**精确的链式法则**，区别只在累积方向。它的做法是：给每个数值额外**携带一个导数分量**（数学上叫对偶数 / dual number），随前向计算一路同步推进，靠解析求导法则（如乘法用 $d(uv)=u\,dv+v\,du$）精确更新。但代价在于：**你必须先选定一个输入方向 $v$**（比如"只扰动参数 $w_5$"），一趟前向只能得到对**这一个方向**的偏导。要拿到对全部参数的偏导，就得换一个方向重跑一趟——有多少参数，跑多少趟。

**于是代价的不对称就出来了。**

|          | 每步运算              | 代价正比于         | 适合           |
| -------- | --------------------- | ------------------ | -------------- |
| 正向模式 | Jvp（雅可比 × 向量） | **输入**个数 | 输入少、输出多 |
| 反向模式 | vJp（向量 × 雅可比） | **输出**个数 | 输出少、输入多 |

判据可以一句话记：**从维度小的那一头起手做连乘**。深度学习训练是最极端的情形——输出只有**一个标量 loss**，输入却是**上亿参数**。从输出那头（种子 $u=1$）左结合起手，全程都是廉价的"行向量 × 矩阵"，一趟反向就拿到全部参数的梯度，代价与参数数量无关。若改用正向模式，就要按参数个数跑上亿趟前向——彻底不可行。这就是为什么训练一律用反向传播。

**那正向模式是不是没用？** 并非如此，它在"输入少、输出多"的场景反而更省。三个典型例子：其一，**二阶优化的 Hessian-向量积（HVP）**——要算 $Hv$ 又不想造出整个 Hessian，可以先用反向模式得到梯度函数 $\nabla f$，再对它沿方向 $v$ 做一次正向模式（forward-over-reverse），一趟拿到 $Hv$，用于 Newton-CG、K-FAC 等；其二，**RNN 的在线学习**——按时间反向传播（BPTT）是反向模式，要存下每个时间步的激活，而实时循环学习（RTRL）是正向模式，沿时间正向推敏感度、**不存历史**，适合无限流；其三，**可微仿真 / 敏感度分析**——少数设计参数对一大片输出场求导，这张"高瘦"雅可比按输入列扫更划算。PyTorch 也提供了正向模式接口 `torch.func.jvp`，只是训练主路用不到它。

**现在把这节接回 §2.1 的反向图，两节就合上了。** §2.1 说每个 grad_fn 节点的 backward "用 saved tensors 算出梯度"，现在可以说得更准：**每个 backward 节点干的，就是一次 vJp $\text{grad\_input} = \text{grad\_output} \cdot J_\text{local}$**。那个从输出端一路左乘过来的行向量 $u$，在工程上就是反向时**从上游传进来的 `grad_output`**；起手的种子 $u=1$，正是标量 loss 的 $dL/dL$。这也解释了一个实战坑：对**非标量**张量直接 `y.backward()` 会报 `grad can be implicitly created only for scalar outputs`——因为输出不是标量时，种子 $u$ 不再天然是 $1$，你得自己传 `y.backward(gradient=u)` 把"输出方向"喂进去。

至于 $\text{grad\_output} \cdot J_\text{local}$ 怎么落地，关键是**从不在内存里真的造出 $J_\text{local}$ 这个矩阵**——这里的"造出"不只是"别逐元素去填它"，而是**连把它整体实例化成一个矩阵对象都不做**；我们利用它的结构，**一步直接算出乘积的结果**（即 $\text{grad\_input}$）。之所以非这样不可，是因为 $J_\text{local}$ 往往大得离谱。

看逐元素的 $y=\exp(x)$（设 $x$ 有 $n$ 个元素）：其 $J_\text{local}$ 是 $n\times n$ 的对角阵 $\mathrm{diag}(y)$。若真把它造出来再乘，就要 $O(n^2)$ 的显存和计算，把一个本该 $O(n)$ 的算子活生生撑爆；而利用"对角"这个结构，$\text{grad\_y}\cdot\mathrm{diag}(y)$ 在纸面上就塌缩成一次 $O(n)$ 的逐元素乘 $\text{grad\_x} = \text{grad\_y} \odot y$，那个 $n\times n$ 矩阵从头到尾不存在。线性层 $y = xW^\top$ 更能让人"看见"这笔内存账——它的完整雅可比要记录"每个输出元素对每个输入元素"的偏导，规模是「输出数 × 输入数」，是个巨大的高维对象。代入具体数字：当 $x$、$W$ 都是 $1024\times1024$ 时，输出和输入各约 $10^6$ 个元素，完整雅可比就有约 $10^6\times10^6 = 10^{12}$ 个元素，单是 fp32 存储就要约 **4 TB**；而这一层真正的 backward 不过是两个矩阵乘、几 MB 的梯度张量。两者差上万亿倍，足见"显式造雅可比"在内存上根本不可行。好在它**分块对角、每块都是 $W$**，vJp 直接塌缩成 $\text{grad\_x} = \text{grad\_y}\cdot W$、$\text{grad\_W} = \text{grad\_y}^\top\cdot x$（正是 §2.0 那条 $Y=XW$ 恒等式的转置变体），那 $10^{12}$ 个元素从头到尾不需要落地。

**一句话收束**：PyTorch 自动微分的精髓，就是**不构造雅可比矩阵，而是为每个算子实现一个 vJp（向量-雅可比积）函数、再沿反向图把它们左结合地串起来**——这正是 reverse-mode 自动微分，本质是一种 **matrix-free（无矩阵）** 的雅可比作用：就像数值线代里的无矩阵迭代法只需要算子作用在向量上的结果 $Av$、从不组装出矩阵 $A$，autograd 也只需要"雅可比作用在梯度向量上的结果"（即 vJp），从不组装出 $J$。代价因此与前向同阶——否则光是造各层的雅可比，训练就根本跑不起来。

这里还藏着一个写新算子时极好用的**自检**：因为 $J_\text{local}$ 本就由前向的操作数搭成，而 vJp 消费的正是这些操作数，所以**"saved tensors"按定义就等于"$J_\text{local}$ 依赖的前向值"**。反过来用——backward 公式里凡是出现、却没在前向 save 的张量，就是 bug（要么漏 save，要么得重算）。

最后给 §2.4 埋个伏笔：反向模式这个"一趟拿全部梯度"的时间便宜，并非没有代价——它是**拿显存换的**。因为反向的计算顺序和前向相反，前向算出的中间量（saved tensors）必须**一直留着**，等反向回头来取；正向模式反而没这负担（导数随算随丢）。这个"时间省下来、显存涨上去"的权衡，就是 §2.4 要算的账。

#### 2.3 Autograd 是如何挂在 dispatch 机制上的

§2.1 我们知道 autograd 在最外层"只记录、不算"，§2.2 又知道它记录的本质是为每个算子实现一次 vJp。但这两件事在**工程上**到底怎么发生的？autograd 既不是另起炉灶的独立系统，也不是 tensor 里藏的某个开关——**它就是 dispatcher 上的一类 key**，和 §1.3 讲的 device/layout 那套 dispatch 是同一套机制。这一节就把它落到 dispatch 上，顺便还清 §1.3 留下的那笔债："`Variable` 和 `Tensor` 合并后，所谓'剥开 variable'到底指什么"。

**autograd 是一个 dispatch key。** 回忆 §1.3：一次算子调用，dispatcher 按 tensor 的 `DispatchKeySet` 里**优先级最高**的 key 落地。`Autograd` 这类 key 的优先级**高于** backend key（`CPU`/`CUDA`/`PrivateUse1`），而它在不在 keyset 里，由输入是否 `requires_grad` 决定。所以只要有输入需要梯度，第一棒一定先落到 autograd。

**一次 `requires_grad` 调用的完整轨迹。** 用 dispatch key 的语言走一遍 `y = op(x)`：

1. **第一次 dispatch → Autograd kernel。** 它干两件事，正是 Ezyang 描述的 *"unwrapping variables, calling the underlying implementation, and then rewrapping the results into variables and recording the necessary autograd metadata for backwards"*——**先记录**（建好 `grad_fn` 节点、存下 saved tensors、用 `next_functions` 连好指向上游的边，即 §2.1 那张反向图），**再 redispatch**，但这次把 `Autograd` key **排除**掉。
2. **第二次 dispatch → backend key。** 排除 autograd 后，keyset 里最高的 key 变成 backend key，于是落到真正的计算 kernel（按 device×layout 选 CPU/CUDA/你的芯片实现），把前向算出来。
3. 算完，autograd kernel 再把 `grad_fn` 挂到输出张量上（`set_history`），返回。

**不会无限循环**的原因就在第 1 步那个"排除"——否则 redispatch 又会选回 autograd，循环不止。

**还债：现代的"剥开 variable"是什么。** §1.3 里我只记下一句"redispatch 时排除 autograd key"，当时没展开。现在补上：2019 之前 `Variable` 是套在 `Tensor` 外的真壳，"剥开"是真去掉一层对象；但现代 `Variable` 和 `Tensor` **已经合并**，根本没有壳可剥了。所以今天的"剥开 variable"**不再是剥对象，而是 redispatch 时把 `Autograd` key 屏蔽掉**这一个动作。Ezyang 那句 *"once you unwrap and go into the non-Variable Tensor universe, that's it; you never go back to Variable"*，对应的就是：autograd key 一旦被屏蔽，这趟调用的剩余部分就一直在 autograd 层**之下**跑，不会再弹回来。

**autograd key 是按后端细分的。** 它不是一个笼统的 `Autograd`，而是 `AutogradCPU`、`AutogradCUDA`、`AutogradPrivateUse1`……所以**你的自研后端有自己专属的 autograd 入口**，这一点在下面"加可导算子"时会用到。

**接本职：让一个自定义算子可导，到底要注册什么？** 这是这节对我最实用的部分。先纠正我自己一个长期的混淆——我一直以为反向也是在 `native_functions.yaml` 里注册的，其实不是。两者是**两个不同 key 上的两次独立注册**：

| 注册什么 | 注册在哪 | 挂在哪个 key |
| --- | --- | --- |
| 算子 + 前向 kernel | `native_functions.yaml`（schema + `dispatch:`） | `CPU` / `CUDA` / `PrivateUse1` |
| 反向公式（导数） | **`tools/autograd/derivatives.yaml`** | codegen 生成的 `Autograd` kernel |

`native_functions.yaml` 只管前向；**反向公式写在 `derivatives.yaml`**，构建时 codegen 据此自动生成 autograd kernel（就是上面"先记录再 redispatch"那个家伙）。如果是自定义 / out-of-tree 算子，则**两个 yaml 都不碰**，改用 `torch.autograd.Function`（自写 forward+backward）或 `torch.library.register_autograd(...)`。

**一个省力的事实：** 反向公式通常是用**别的 ATen 算子**表达的（`mul` 的反向就是两个 `mul`），而这些算子在你后端上**已经有 kernel**。所以只要你把 backward 写成现有算子的组合，它会自动 dispatch 回你的后端、**"免费"获得可导性**，你不必为反向再单独写一个芯片 kernel——只有当反向需要一个全新的底层原语时，才得在芯片上实现一个 backward kernel。

**no_grad 为什么能省显存。** 既然 autograd 只是最外层一个 key，那把它关掉就是一件很轻的事：`torch.no_grad()` / `inference_mode()` 通过线程局部状态（TLS）**从一开始就把 `Autograd` key 排除**，于是连第 1 步的记录都不发生——不建 `grad_fn`、不存 saved tensors，输出张量 `requires_grad=False`。这既省显存又稍快。`inference_mode()` 更狠，连版本号、view 追踪都省掉。而"saved tensors 一旦不建就省下的那块显存"有多大、训练时又怎么权衡，正是下一节 §2.4 要算的账。

<details>
<summary><b>进阶：dispatcher 内部的 TLS / RAII 机制（普通读者可跳过）</b></summary>

上面说"把 autograd key 排除掉"，底层是怎么实现的？涉及两个 C++ 概念。

**RAII** 是 C++ 习语：把状态的获取与释放绑到一个对象的构造函数与析构函数上，对象一离开作用域（正常结束**或**抛异常）就自动还原——相当于 C++ 版的 `with` 块。

**被它操纵的 TLS 状态**：每个线程有一份 `c10::impl::LocalDispatchKeySet`，内含两个集合：

```cpp
struct LocalDispatchKeySet {
  DispatchKeySet included_;  // 强制「加上」的 key
  DispatchKeySet excluded_;  // 强制「去掉」的 key
};
// 最终 keyset ≈ (输入 tensor 的 keyset │ included_) − excluded_，再取最高优先级
```

把 `Autograd` 塞进 `excluded_`，就等于"这一刻当 tensor 没带 autograd"——而 tensor 自身的 keyset 一个字节没动。

**具体的卫士（由内到外）**：`ExcludeDispatchKeyGuard`/`IncludeDispatchKeyGuard`（底层原语）→ `AutoDispatchBelowADInplaceOrView`（codegen redispatch 前用，老名 `AutoNonVariableTypeMode` 已废）→ `AutoGradMode(false)`（`no_grad` 的真身，翻 `GradMode` TLS）→ `InferenceMode`（更狠，连 `ADInplaceOrView` 也排除）。

**在生成代码里长这样**（简化）：

```cpp
// torch/csrc/autograd/generated/VariableType_*.cpp（自动生成，简化）
at::Tensor mul_Tensor(c10::DispatchKeySet ks,
                      const Tensor& self, const Tensor& other) {
  // 1) 记录：建反向节点 + 存 saved tensors + 连边
  auto grad_fn = std::make_shared<MulBackward0>();
  grad_fn->set_next_edges(collect_next_edges(self, other));
  grad_fn->self_  = SavedVariable(self,  /*is_output=*/false);
  grad_fn->other_ = SavedVariable(other, /*is_output=*/false);

  // 2) redispatch 到 autograd 之下
  auto result = ([&]() {
    at::AutoDispatchBelowADInplaceOrView guard;              // RAII：TLS 里排除 autograd
    return at::redispatch::mul(ks & c10::after_autograd_keyset, self, other);
  })();                                                       // lambda 返回，guard 析构，TLS 自动恢复

  // 3) 把记录挂回结果
  set_history(result, grad_fn);   // result.grad_fn = grad_fn; requires_grad = true
  return result;
}
```

这里有**两道防循环保险**并存：① keyset 参数 `ks & after_autograd_keyset`——透传的 `DispatchKeySet` 里直接抹掉 autograd，这次 dispatch 从计算上就选不到它；② TLS 卫士——覆盖 redispatch **内部再发生的嵌套调用**（backend kernel 里又调别的算子时也不会重新触发 autograd）。

**为什么非 RAII + TLS**：TLS 保证线程隔离（多线程各跑 autograd 不串味）；RAII 保证异常安全——backend kernel 若在 redispatch 里抛异常，`guard` 析构照样执行、TLS 照样恢复，绝不残留"autograd 被永久屏蔽"的脏状态。

**调试钩子**：排查"某算子没建反向图 / `grad_fn` 是 None"时，多半是某层 `excluded_` 把 `AutogradPrivateUse1` 蒙住了（常见元凶：外面套了 `no_grad`/`inference_mode`，或某段 C++ 残留了一个 `AutoDispatchBelowAutograd` 卫士）——去 `c10::impl::tls_local_dispatch_key_set()` 看 `included_`/`excluded_` 里有什么。

</details>

#### 2.4 saved tensors 的内存代价：激活显存、重计算与 in-place 陷阱

§2.2 末尾我说反向模式的时间便宜是"拿显存换的"，§2.3 末尾又说 `no_grad` 省下的正是这块——这一节就把这笔显存账算清。它也是整章里对做训练/推理系统的人最贴身的一节。

**saved tensors 就是"激活显存"。** §2.2 讲过，反向的计算顺序和前向相反，所以前向算出的中间值（saved tensors）必须**一直留到反向**才能释放。这批留驻的中间值，就是训练显存里那块叫**激活（activations）**的东西——前向走多深、留得就多深。于是反向模式虽然时间上一趟拿全部梯度，却要在整个前向期间扛着这批激活，这就是它的代价。

围绕"怎么管理这块激活显存"，有**三个方向的杠杆**，代价各不相同：

| 杠杆 | 做法 | 拿什么换 |
| --- | --- | --- |
| **不存 → 重算** | gradient checkpointing | 算力（多一遍前向） |
| **就地存 → 省分配** | in-place 操作 | autograd 正确性的风险 |
| **挪走存 → 换介质** | saved tensors offload | CPU/NVMe 带宽 |

**① 不存 → 重算（gradient checkpointing）。** 思路是：前向时**故意不存**某些中间激活，等反向需要它们时，**重新跑一遍那段前向**把它们算回来。经典做法对 $L$ 层网络只在 $O(\sqrt{L})$ 个边界存激活、其余重算，把激活显存从 $O(L)$ 压到 $O(\sqrt{L})$，代价约是**多一遍前向（≈33% 额外算力）**。PyTorch 的接口是 `torch.utils.checkpoint`，它内部正是 §2.3 那套机制——重算那段前向时用一个类似 `no_grad` 的环境跑、不建图，只在真正需要的边界处重新挂上 autograd。

**② 就地存 → 省分配（in-place）+ version counter 陷阱。** in-place 操作（`x.add_()`、`relu_()`）直接改写原 storage、省掉一次分配。但它有个陷阱：**如果被改的张量正是某个算子 save 起来留作反向用的，反向时就会读到被污染的值**。PyTorch 用 **version counter** 来兜底：版本号绑在底层 storage 上（`tensor._version` 可读），`SavedVariable`（§2.3 那个存档对象）在 save 时记下当时的版本，反向解包时拿当前版本一比，不一致就抛错：

```text
one of the variables needed for gradient computation has been modified by an
inplace operation: ...; expected version N but got version M
```

这里要记住 version counter 的真正价值：**它不是帮你算，是帮你拦**——把"静默地算出错误梯度"（最难查的 bug）转成"当场报错、还告诉你期望版本 N、实际 M"（一眼定位）。

**③ in-place 到底什么时候安全？** 由上可得一条判据（写自定义算子时直接能用）：

> 一个算子能安全地做 in-place，当且仅当它的 **backward 不依赖任何会被这次原地写覆盖掉的值**——等价地说，backward 只依赖**输出**（或什么都不依赖），而不依赖被改写的**输入**。

落到三种情形：① 张量**无 grad / 没被 save** → 随便改，还省一次分配；② backward 只用**输出**（如 `relu_`、`exp_`，导数靠输出就能算）→ 安全，PyTorch 允许；③ **叶子张量且 `requires_grad=True`** → 直接禁止，报 `a leaf Variable that requires grad is being used in an in-place operation`。实操上有个捷径：**看你的 derivative 公式里出现的是 `self`（输入）还是 `result`（输出）**——只出现 `result` 就能放心提供 in-place 变体；一旦出现 `self`，in-place 变体要么禁掉、要么得先把输入克隆一份留作 saved（那就没省到分配了）。

**④ 挪走存 → 换介质（offload）。** 第三个杠杆是 `torch.autograd.graph.saved_tensors_hooks`：注册一对 pack/unpack 钩子，把 saved tensors 在前向后**搬到 CPU/NVMe**、反向前再搬回，拿带宽换显存。它和重算是两种正交的省法——一个不存（省到底但费算力），一个挪走（仍存但不占显存，费带宽）。

至此 §2 自动微分四节（数学预备 → 记录什么 → 为什么反向 → 挂在 dispatch 上 → 显存账）全部走完。而 saved tensors 这块"激活"只是训练显存的一部分——既然算到这里，不妨把训练显存的**全局分布**也一并铺开，看看不同场景下钱都花在哪。

##### 扩展：训练显存量分布与多场景占比

**先把显存切成两大类**，分界线是"它的大小受不受 batch 影响"：

| 类别 | 包含 | 随什么增长 | 受 batch 影响 |
| --- | --- | --- | --- |
| 模型状态 model states | 参数 + 梯度 + 优化器状态 | 参数量 $P$、优化器、精度 | ❌ |
| 激活 activations | 前向留给反向的中间值（saved tensors） | $b \times s \times h \times L$ | ✅ |
| （残留/临时） | 通信桶、kernel 临时 buffer、碎片、CUDA context | 杂项 | 部分 |

这条线是钥匙：**模型状态是固定成本，激活是可变成本**，谁主导决定了你该用哪种省法。

**模型状态——一笔每参数的固定账。** 以 Adam + 混合精度为例：

| 项 | 字节/参数 |
| --- | --- |
| fp16 权重 | 2 |
| fp16 梯度 | 2 |
| fp32 master 权重 | 4 |
| fp32 一阶动量 $m$ | 4 |
| fp32 二阶动量 $v$ | 4 |
| **合计** | **16 B/参数** |

**优化器状态（master + $m$ + $v$ = 12B）占了 3/4**，是模型状态的绝对大头——这也是为什么我把问 1 里的"训练数据"修正成了"优化器状态"。换算：1B 模型 → 16 GB，7B 模型 → **112 GB**（已超单卡，故非分片不可）。换配置这张表就变：SGD+momentum 约 12 B/参数；8-bit Adam（$m$/$v$ 压到 int8）约 8 B/参数；LoRA/PEFT 把冻结基座的梯度与优化器状态**砍光**（基座只留 2B 的 fp16 权重），只有极小的适配器吃满 16B——但它**一点没省激活**。

**激活——一笔随 batch 与序列膨胀的可变账。** 激活不直接随 $P$ 走，而随 $b \times s \times h \times L$。对 Transformer，每层激活量近似为（Megatron《Reducing Activation Recomputation》）：

$$ \text{每层} \approx s\,b\,h\left(34 + 5\,\frac{a\,s}{h}\right) \text{字节}\quad(a=\text{注意力头数}) $$

两个要点：它**线性正比于 batch $b$**（减 batch 直接降激活）；括号里 $5as/h$ 项来自注意力分数矩阵、带一个 **$s^2$**——所以**长上下文训练里激活会被注意力炸上天**，这正是 FlashAttention（不实例化 $s \times s$ 分数矩阵）和序列并行的动机。

**多场景下谁主导（核心）：**

| 场景 | 主导块 | 为什么 | 对症手段 |
| --- | --- | --- | --- |
| 大模型 + 小 batch（LLM 预训练/全参微调） | 模型状态 | $16P$ 巨大、激活相对小 | ZeRO/FSDP、优化器 offload、8-bit Adam |
| 小模型 + 大 batch（BERT 大批量、视觉高分辨率） | 激活 | $b$ 大、$P$ 小 | checkpointing、减 batch、激活 offload |
| 长上下文训练 | 激活（注意力 $s^2$） | $5as/h$ 随 $s^2$ 爆炸 | FlashAttention、序列并行、重算 |
| LoRA/PEFT 微调 | 激活 + 冻结权重 | 优化器状态被砍光、前向激活照旧 | 重算 + 量化基座（QLoRA） |
| **推理** | 参数 + KV cache | 无梯度/优化器/反向激活，KV cache 随 $b\cdot s\cdot L\cdot h$ 涨 | PagedAttention、KV 量化、KV offload |

**把省显存手段对回"砍哪一块"**，就是一张完整作战图：

| 手段 | 砍哪块 | 拿什么换 |
| --- | --- | --- |
| gradient checkpointing | 激活 | 算力 |
| in-place | 激活（省分配） | autograd 正确性风险 |
| `saved_tensors_hooks` offload | 激活 | CPU/NVMe 带宽 |
| ZeRO-1/2/3、FSDP | 模型状态（优化器/+梯度/+参数） | 通信量 |
| 8-bit / online 优化器 | 优化器状态 | 少量精度 |
| 张量并行 / 序列并行 | 参数 + 激活 | 卡间通信 |
| FlashAttention | 激活的注意力 $s^2$ 项 | 重算 |

**一句收束。** 推理那行最值得玩味：`no_grad` 一开就省掉了优化器状态与反向激活（正是 §2.3 那套从 TLS 排除 autograd），于是显存只剩**参数 + KV cache**，而 KV cache 成了新的"可变大头"。可见 **autograd 的激活账（训练侧）与 KV cache 账（推理侧），本质是同一个问题——"中间状态该存多少、怎么存"——在两个战场上的两个化身。** 这也把这一整章的训练视角，接回了你主战场的推理视角。

### 3. 基本代码结构

### 4. 编写算子

### 5. Pytorch中高效的工作流

## 读后回顾

> 完整学完一遍后回头收口。

- 回答先前提出的疑问：
- 对比我的直觉与资料给出的思路办法（看看读之前的我有多天真）：

## 实践（纯理论板块改成手算 / 反例构造 / 数值验证）

> 小型实验验证、加深理解。工作量大时可延后到节假日补，不必首发即带。

## 下游透镜

> 把知识接到两个真实场景，让它不止停在"学了"和"demo"。

### 过往经验

> 与过去工作相关时，分享处理经验（向后接：用新知识回看旧经验）。不一定普适，仅供参考。

### 面试问题Q&A

> 构造几道可能被问到的面试题 + 我的理解（向前用）。不一定准确，欢迎读者补充指正。

- **Q：一次 `torch.add(a, b)` 调用会经过哪些 dispatch 层？**
  A：从外到内是 variable(autograd) → backend(device × layout) → kernel 内的 dtype switch。variable 层只在有输入 `requires_grad=True` 时才真正介入（为反向传播做记录），否则相当于透传。
- **Q：连续和非连续的 dense tensor，调同一个算子会 dispatch 到同一个 kernel 吗？**
  A：会。layout 调度看的是 `Layout` 枚举（Strided/Sparse/Mkldnn）这种整体类型，不看连续性。连续性在 kernel 内部处理——element-wise 走 TensorIterator 按 stride 读，或某些算子先 `.contiguous()`。
- **Q：为什么 PyTorch 给一个算子要准备这么多份 kernel？**
  A：因为 device × layout × dtype 是一个笛卡尔积，每个组合原则上都可能需要一份特定实现。
- **Q：自研 PrivateUse1 后端的某算子只实现了 float32，用户传 bfloat16 会怎样、怎么修？**
  A：dispatcher 会成功把调用送到该 kernel（device + layout 匹配上了），随后在 kernel 内部的 `AT_DISPATCH_*` 默认分支抛错 `not implemented for 'BFloat16'`——并非 dispatcher 级的 backend 报错。修法是把 `AT_DISPATCH_FLOATING_TYPES` 换成 `AT_DISPATCH_FLOATING_TYPES_AND2(Half, BFloat16, ...)`，而不是注册新的 dispatch key。
- **Q：反向传播为什么不直接构造雅可比矩阵？它的替代方案是什么？**
  A：不构造，是因为完整雅可比的规模 =「输出数 × 输入数」，往往大到不可行——一个 $1024\times1024$ 的线性层，其雅可比约 $10^{12}$ 个元素、fp32 约 4 TB，而它真正的 backward 只是几 MB 的矩阵乘；何况训练只要标量 loss 对参数的梯度，并不需要整个 $J$。替代方案是 **matrix-free（无矩阵）的 vJp（向量-雅可比积）**，分三层：① **算子级**——每个算子配一个 backward 规则，直接算出 $\text{grad\_input} = \text{grad\_output}\cdot J_\text{local}$ 这个乘积的闭式结果（用矩阵求导离线推好、利用 $J_\text{local}$ 的结构塌缩成逐元素乘或矩阵乘），只返回"作用在向量上的结果"、从不返回 $J$，并 save 必要的前向张量；② **记录级**——前向时给输出张量挂 `grad_fn`（封装这个 vJp 函数 + saved tensors + 指向上游的边），即时建出反向图；③ **装配级**——`backward()` 从输出端种子 $u=1$ 起，沿反向图把各算子的 vJp 左结合地串起来（即链式法则连乘），节点间只流动梯度向量。一句话：不求 $J$、只求 $J^\top$ 对向量的作用，逐算子实现、整图串联——这就是 reverse-mode 自动微分，代价与前向同阶。

## 思维导图总结

> 把整体思路凝练成思维导图，便于后续快速回顾。

## 后续预告

- 依旧迷惑的问题：
- 由此延伸出的想法：
- 下一节博文预告：
