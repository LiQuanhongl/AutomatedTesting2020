# AutomatedTesting2020

姓名：黎泉宏

学号：181250063

选题方向：移动应用大作业

***





## 模型分析



### 模型结构

使用yolov3模型进行训练。

yolov3由53个卷积层组成，其结构如下所示：

![](https://lqhoss.oss-cn-beijing.aliyuncs.com/yolov3.PNG)





### 运行步骤

#### 第一阶段：数据解析

程序入口：Project\stage1\parseJson.py

步骤：

1、将ATMobile2020-1.zip解压，然后把ATMobile2020-1文件夹复制到Project\stage1\里

2、运行parseJson.py

3、得到stage1_output文件夹即为标注后的数据集（得到的stage2_pre和yolo_data文件夹用于第二阶段）

输出的文件是每个图片含有的控件类别和左上角、右下角坐标

#### 第二阶段：控件识别

##### 模型训练

步骤：

1、将第一阶段得到的yolo_data文件夹中的images文件夹、labels文件夹、train.txt、valid.txt复制到Project\stage2\PyTorch-YOLOv3\data\custom中。

2、下载预训练权重文件darknet53.conv.74 （地址： https://lqhoss.oss-cn-beijing.aliyuncs.com/darknet53.conv.74 ）放到Project\stage2\PyTorch-YOLOv3\weights中。

3、在Project\stage2\PyTorch-YOLOv3运行以下命令安装所需环境

```
pip3 install -r requirements.txt
```

4、在Project\stage2\PyTorch-YOLOv3运行以下命令开始训练

```
python3 train.py --model_def config/yolov3-custom.cfg --data_config config/custom.data --pretrained_weights weights/darknet53.conv.74
```

5、训练过程中的模型保存在checkpoints文件夹中

##### 使用已训练的模型识别控件

步骤：

1、将要识别的图片放在Project\stage2\PyTorch-YOLOv3\data\samples中。

2、下载我训练好的模型（地址：https://lqhoss.oss-cn-beijing.aliyuncs.com/my_model.pth ），将其放到Project\stage2\PyTorch-YOLOv3\weights中。

3、在Project\stage2\PyTorch-YOLOv3运行以下命令开始识别

```
python3 detect.py --image_folder data/samples/ --weights_path weights/my_model.pth --model_def config/yolov3-custom.cfg --class_path data/custom/classes.names 
```

4、经过标注的截图和对应描述截图的文件都保存在output文件夹中。

输出的是经过标注的截图和对应的json文件，json文件中num是识别出来的控件数量，object是各个控件的描述

### python及第三方库版本

#### 第一阶段：

python 3.7

Pillow

#### 第二阶段：

python 3.7

Pillow

tensorflow 2.3.0

numpy

torch>=1.0

torchvision

matplotlib

terminaltables

tqdm

### 相关参考文献

Object Detection for Graphical User Interface: Old Fashioned or Deep Learning or a Combination?

YOLOv3: An Incremental Improvement

## 实验验证



### 评估指标及含义

TP:True Positive，IoU大于某个值时的检测框数量

FP:False Positive，IoU小于或等于某个值时的检测框数量

FN:False Negative，没有检测到ground truth的数量

Precision:查准率，计算公式为TP/(TP + FP)

Recall:召回率，计算公式为TP/(TP + FN)

AP:某一个类别P-R曲线下的面积

mAP:所有类别 P-R 曲线下面积的平均值

### 验证结果

对800张数据进行训练，但效果并不理想，训练了60轮epoch左右，mAP的值一直在0.6~0.7左右变化

## 结果示例

![](https://lqhoss.oss-cn-beijing.aliyuncs.com/343.png)

对应的json文件为，num是识别出的控件数量，object里是控件描述，class是控件的类，left_top是左上角坐标，right_bottom是右下角坐标

```
{
    "num": 7,
    "object": [
        {
            "class": "ImageView",
            "left_top": [
                29,
                889
            ],
            "right_bottom": [
                131,
                993
            ]
        },
        {
            "class": "ImageView",
            "left_top": [
                38,
                1026
            ],
            "right_bottom": [
                128,
                1116
            ]
        },
        {
            "class": "ImageView",
            "left_top": [
                38,
                1161
            ],
            "right_bottom": [
                128,
                1248
            ]
        },
        {
            "class": "ImageView",
            "left_top": [
                35,
                1410
            ],
            "right_bottom": [
                121,
                1496
            ]
        },
        {
            "class": "ImageView",
            "left_top": [
                37,
                1545
            ],
            "right_bottom": [
                125,
                1636
            ]
        },
        {
            "class": "Button",
            "left_top": [
                991,
                67
            ],
            "right_bottom": [
                1070,
                217
            ]
        },
        {
            "class": "ImageView",
            "left_top": [
                26,
                1661
            ],
            "right_bottom": [
                141,
                1780
            ]
        }
    ]
}
```



## 个人感想

模型训练的效果并不理想，可能是由于第一阶段所得到的控件数量不多，一些类别的控件数量甚至低于100，导致模型可能训练得不好。