# PDF处理经验分享
## 2020-5-4-17：48-PM 视频来了

模糊不清？体积太大？不能复制？手把手教你优化 PDF 电子书\_哔哩哔哩 (゜ - ゜) つロ 干杯~-bilibili

## 案例效果预览：

![](https://img2.doubanio.com/view/note/l/public/p72058991.jpg)

![](https://img9.doubanio.com/view/note/l/public/p72058995.jpg)

使用的工具有：：PdfPatcher， Adobe Acrobat， ComicEnhancerPro，Freepic2Pdf，PDFXEdit，ABBYY Finereader 14OCR 编辑器。

![](https://img1.doubanio.com/view/note/l/public/p72056317.jpg)

## 无图 PDF 的处理

### 1. 利用 PdfPatcher 提取文档内图片

![](https://img2.doubanio.com/view/note/l/public/p72056323.jpg)

如果发现提取出图片不正常（如全黑），文件名混乱，或多页使用同一图片等情况，可以考虑使用 Adobe Acrobat 的另存为图片功能。

![](https://img9.doubanio.com/view/note/l/public/p72056346.jpg)

2\. 使用 ComicEnhancerPro 对提取图片进行处理

此软件有很多设置选项，这里仅对个人常用的几处进行讲解：

![](https://img3.doubanio.com/view/note/l/public/p72056420.jpg)

其他 - 色彩 - 色彩数：我处理电子书的第一部就是将这里设置为纯黑白，这是关键的一部，此步作用为将图片二值化，缩小图片存储大小，提高文字锐度。

其他 - 色彩 - 去斑直径：消除指定像素大小以下的黑点。

其他 - 色彩 - 去除与边缘接触的黑色区域：去除图片黑边。

其他 - 色彩 - 边缘去毛刺：使内容显示更柔和。

![](https://img1.doubanio.com/view/note/l/public/p72056439.jpg)

曲线 - 设置：调整图片的颜色和色调，我一般最后才拉微调曲线。

![](https://img9.doubanio.com/view/note/l/public/p72056446.jpg)

缩放：顾名思义，调整图片分辨率，个人一般拉到 120%

![](https://img2.doubanio.com/view/note/raw/public/p72056451.gif)

其他 - 调节 - 高斯模糊半径和高斯锐化半径：这两处滑块可以同步拖动，如拉高了模糊半径，就拉高点锐化半径看看效果。

![](https://img1.doubanio.com/view/note/l/public/p72056468.jpg)

USM 锐化：一种锐化图片边缘的技术，一般我将遍数设置为 3，数量随意拉到 165 左右，半径随意拉到 35 左右就不再更改，然后拖动阈值直到达到满意效果。

![](https://img2.doubanio.com/view/note/l/public/p72056501.jpg)

文件 - 批量转换：完成以上步骤就可以批量转换了，注意保存扩展名要选择位图格式 tif。

### 3. 使用 Freepic2Pdf 将转换成功的图片合并为 Pdf

![](https://img9.doubanio.com/view/note/l/public/p72056506.jpg)

(完）

## PDF 内图片内容的处理

### 1. 走一遍无图 PDF 的处理流程

### 2. 使用 ABBYY Finereader 14OCR 编辑器提取 PDF 的图片内容

![](https://img1.doubanio.com/view/note/l/public/p72056507.jpg)

部分不能精准识别需要手动框选，之后以 html 格式保存。嫌识别速度慢的可以设置为[仅识别图片](https://support.abbyy.com/hc/en-us/articles/360003394019-Extracting-Pictures-from-the-Document)。

### 3. 使用 PDFXEdit 将图片一张一张覆盖到处理过的 PDF 里。

![](https://img3.doubanio.com/view/note/l/public/p72056510.jpg)

CtrlCV 即可，因为保存的图片排序和原始文档的顺序一样，此步实际耗时不多。

### （完）

## 视频

其实上面截图来自我前天录的一个十几分钟的视频，讲解要比上面详细很多。有时间剪剪发到 b 站吧。

### （完）

最后，放一下开头案例的设置参数。

![](https://github.com/yuukoamamiya/pic-for-memo/blob/main/img/2022-1-11%2020-38-03/c8d2cd05-cc25-49d8-aca5-17aed15a1c0c.jpeg?raw=true) 
 [https://www.douban.com/note/760704793/?\_i=1904675zr2il_W](https://www.douban.com/note/760704793/?_i=1904675zr2il_W)
