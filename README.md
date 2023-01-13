# 数据集格式转换工具V3.0

> 基于PaddleX完善的数据集格式转换工具

## Introduction

这是数据集格式转换工具的第三次重构。与上次重构的变化是，不再使用参数的方式运行特定脚本，在实际经验中，改代码比改参数更方便，效率更高。且相比原版添加代码需大费周章地进tools添加对应的类，在init暴露，再在convert脚本中写参数对应关系，类中只保留生成数据集格式所需的必要函数外，一个任务一个脚本，编写脚本更有效率。

`数据集指南`中会记录各数据集的目录与编码格式，以方便查阅学习和脚本编写参考。希望这个小玩意可以帮你增加工作效率。


## Start

### 1️⃣ 安装依赖

```bash
pip install -r requirement.txt
```

### 2️⃣ 按样例`template.py`编写转化脚本

### 3️⃣ 运行脚本

## 数据集指南

### COCO

#### 目录结构：

- annotations
  - `instances_train2017.json`
  - `instances_val2017.json`
  - `instances_test2017.json`
- images
  - train2017
    - `EDD2020_ACB0001.jpg`
    - ...
  - val2017
  - test2017
- `labels.txt`

#### json结构：

```json
{
    "images": [
        {
            "height": int,
            "width": int,
            "id": int,
            "file_name: 'str'
        }
    ],
    "categories": [ # 分类
        {
            "id": int,
            "name": str, # 子类别
            "supercategory": str  # 主类别：如山羊、绵羊都属于羊，但我们使用时倾向于将此处设置为component
        }
    ]，
    "annotations": [
        {
            "id": int # 标注对象id，每一个对象的id是唯一的
            "segmentation": [  # mask
                float, float,  # 第一个点的x, y坐标
                float, float
            ],
            "iscrowd": int, # 0 or 1，是否为大组对象
            "area": float, # 区域面积
            "bbox": [float, float, float, float],    # 检测边框[x,y,w,h]
            "image_id": int,  # 图片ID
            "category_id": int  # 类别ID
        }
    ]
}
```

### EDD


### KC


### YOLO

#### 目录结构

- train
  - `1.jpg`
  - `1.txt`
  - ...
- val
- test
- `labels.txt`

#### txt标注结构

```
类别id（从0开始） 归一化后的中心x 归一化后的中心点y 归一化后的框宽度 归一化后的框高都
```

