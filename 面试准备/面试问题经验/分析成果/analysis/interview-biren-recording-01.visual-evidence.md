# 壁仞科技面试记录：画面证据核查

核查日期：2026-11-17。记录 ID：`interview-biren-recording-01`。

源文件：[壁仞科技.mkv](/root/workspace/learning/daily-work/work/managed/interview-video-analysis/incoming/壁仞科技.mkv)。本次仅在本地抽取并查看静帧，没有上传画面，没有改写原视频或既有图片，也没有修改 manifest。

## 可直接使用的结论

在 **00:13:00—00:15:25 的采样画面**中，在线面试编辑器里有逐步增加的 Attention／缓存相关笔记。**00:15:25** 的笔记区完整可见，可确认输入维度、`linear`、`cache`、K/V/Q 维度记号及 `softmax(Q*K^T)*V` 这一行。这里的“完整可见”指该帧中这些笔记的完整行文可见，不代表完整技术推导、完整源代码或整场面试过程都已经呈现。

**00:15:30—00:41:00 的所查采样点**均出现中央通话浮窗，编辑器大部分区域被遮挡且背景变暗；左侧第 6—12 行仍可辨认，和 00:15:25 的笔记一致。不能由离散采样断言这段时间始终没有操作，也不能推断被遮挡区域的内容。

00:41:20 已显示本地录屏软件及本地笔记界面，不能把这帧的本地准备材料当作面试中已经说出或展示的答案。

## 公式与字符记录

依据 [00:15:25 笔记裁剪图](/root/workspace/learning/daily-work/work/managed/interview-video-analysis/derived/interview-biren-recording-01.frame-15m25s.notes-crop.png)，可读笔记如下。空格按阅读整理，未将简写扩展为正式公式。

```text
x [T, H]
x linear-> x_l [T, h] (k,v)
x_l -> cache
x_l -> k [T, D_k]
x_l -> v [T, D_v]
x -> Q [T, D_q]
softmax(Q*K^T)*V
```

- `x_l` 下划线后的窄字符在像素图中形似小写 `l`，也可能被读作数字 `1`；这里保留近似转录，不将该字符名称作为判断依据。
- 输入的 `H` 与下一行的 `h` 大小写可区分；`cache`、`linear`、`softmax` 及 K/V/Q 相关记号可辨认。
- 00:15:00 第 12 行仍为空；00:15:10 可见公式开始输入；00:15:20 可见 `softmax(Q*K^T)`；00:15:25 可见末尾 `*V`。这些是采样时点的画面状态，不是每次键入的精确开始时间。
- 该可见公式行没有写出缩放分母或 mask。**这只能说明屏幕简写未呈现这些项，不能据此判定口头说明遗漏、知识错误或技术能力不足。**
- 画面没有提供可运行程序、测试用例或执行结果；不能把这些笔记称为已完成并验证的 Attention 实现。
- 这里只记录屏幕上出现的内容，不仅凭画面认定是哪一方输入、解释或纠正。相关归属应与有时间定位的音频证据交叉核对。

![00:15:25 的笔记区，仅裁剪与整数倍放大](/root/workspace/learning/daily-work/work/managed/interview-video-analysis/derived/interview-biren-recording-01.frame-15m25s.notes-crop.png)

## 采样时间与可见范围

所有时间均为原视频起点起算的时分秒，非桌面显示的墙上时钟。视频为 1280×720、30 fps；表中时间是 FFmpeg 的精确定位请求值，帧时间粒度约为 33 毫秒。本次没有逐帧核查两个采样点之间的完整变化。

| 采样时间 | 可见内容 | 证据边界 |
| --- | --- | --- |
| 00:10:00（既有图） | 在线编辑器和中央通话窗 | 所查笔记尚未出现；不能推断其他时间的内容 |
| 00:13:00 | `x [T,H]`、`x linear-> [T,h] (k,v)` | 笔记完整可见，右侧视频小窗未覆盖这些行 |
| 00:15:00 | 加入中间量、`cache`、K/V/Q 维度记号 | 第 6—11 行完整可见，第 12 行为空 |
| 00:15:10 | 第 12 行开始输入公式，可见 `Q*` | 编辑过程中的临时状态，不能作为最终公式 |
| 00:15:20 | 第 12 行可见 `softmax(Q*K^T)` | 光标处于公式内；尚未见末尾 `*V` |
| 00:15:25 | 可见 `softmax(Q*K^T)*V` | 笔记完整可见，是本次公式核查的主要证据 |
| 00:15:30、00:16:00、00:16:30 | 中央通话窗覆盖编辑器，左侧笔记仍可读 | 背景变暗，不能核查浮窗覆盖部分 |
| 00:18:00、00:20:00、00:22:00、00:24:00 | 同一组左侧笔记仍可见 | 中央和右侧部分被通话窗遮挡 |
| 00:25:00（既有图）、00:28:00、00:30:00 | 同一组左侧笔记仍可见 | 不能据此断言整个时间段没有其他操作 |
| 00:38:00（既有图）、00:40:00、00:41:00 | 同一组左侧笔记仍可见 | 未发现新的可读公式行；仍有遮挡 |
| 00:41:20 | 本地录屏软件与本地笔记界面 | 不作为面试现场作答内容引用，不转录其中个人信息 |

## 提取方法与新增图片

完整帧通过本地 FFmpeg 6.1.1 提取，使用 `-ss <秒数> -i <原视频> -map 0:v:0 -frames:v 1 -update 1 -n <新图片>`。`-n` 防止覆盖已存在的输出。

裁剪图仅使用原始抽帧图的裁剪与最近邻 4 倍放大，没有生成、补写或锐化字符，也没有调亮暗背景。00:15:00、00:15:20、00:15:25 的裁剪为 `crop=300:120:108:228,scale=1200:480:flags=neighbor`；00:18:00 的裁剪为 `crop=210:120:100:228,scale=840:480:flags=neighbor`。这些裁剪均不包含人脸、账号、浏览器地址或个人姓名。

新增 17 张完整帧与 4 张裁剪图，目录均为：

`/root/workspace/learning/daily-work/work/managed/interview-video-analysis/derived/`

| 原视频时间 | 新增文件名 |
| --- | --- |
| 00:13:00 | `interview-biren-recording-01.frame-13m00s.png` |
| 00:15:00 | `interview-biren-recording-01.frame-15m00s.png` |
| 00:15:10 | `interview-biren-recording-01.frame-15m10s.png` |
| 00:15:20 | `interview-biren-recording-01.frame-15m20s.png` |
| 00:15:25 | `interview-biren-recording-01.frame-15m25s.png` |
| 00:15:30 | `interview-biren-recording-01.frame-15m30s.png` |
| 00:16:00 | `interview-biren-recording-01.frame-16m00s.png` |
| 00:16:30 | `interview-biren-recording-01.frame-16m30s.png` |
| 00:18:00 | `interview-biren-recording-01.frame-18m00s.png` |
| 00:20:00 | `interview-biren-recording-01.frame-20m00s.png` |
| 00:22:00 | `interview-biren-recording-01.frame-22m00s.png` |
| 00:24:00 | `interview-biren-recording-01.frame-24m00s.png` |
| 00:28:00 | `interview-biren-recording-01.frame-28m00s.png` |
| 00:30:00 | `interview-biren-recording-01.frame-30m00s.png` |
| 00:40:00 | `interview-biren-recording-01.frame-40m00s.png` |
| 00:41:00 | `interview-biren-recording-01.frame-41m00s.png` |
| 00:41:20 | `interview-biren-recording-01.frame-41m20s.png` |
| 00:15:00 裁剪 | `interview-biren-recording-01.frame-15m00s.notes-crop.png` |
| 00:15:20 裁剪 | `interview-biren-recording-01.frame-15m20s.notes-crop.png` |
| 00:15:25 裁剪 | `interview-biren-recording-01.frame-15m25s.notes-crop.png` |
| 00:18:00 裁剪 | `interview-biren-recording-01.frame-18m00s.notes-crop.png` |

已查看全部新增图片及既有 00:10:00、00:25:00、00:38:00 三张图片。未据人脸、姿态或表情推断情绪、人格、诚实程度或技术能力；未转录画面中的姓名、账号、邮箱或通话标识。完整抽帧仍包含源画面的原始信息，仅作为本地核查材料保留。
