import pandas as pd
import os
from tools import *

origin_dir = 'datasets/KC'
output_dir = 'output/KC2'

df = pd.read_csv(os.path.join(origin_dir, 'metadata.csv'), sep = ';')
df = df[df['x1'].notna()]

# print(df)
print(df['finding_class'].value_counts())

images_origin= df['filename'].tolist()
images = []
for i in images_origin:
    images.append(os.path.join('datasets/KC/images', i))

# 数据集拆分
os.path.join(output_dir, 'split_result')
if not(os.path.exists(os.path.join(output_dir, 'split_result'))):
    dataset_split(images, train=0.8, val=0, test=0.2, outputDir=output_dir, mode=1)
if not(os.path.exists(os.path.join(output_dir, 'annotations'))):
    os.makedirs(os.path.join(output_dir, 'annotations'))

coco_annotations = os.listdir(os.path.join(output_dir, 'split_result'))
categories=[]
category_list=[]
for coco_class in coco_annotations:
    output_image_dir = os.path.join(output_dir, 'images', coco_class+'2017')
    if not(os.path.exists(output_image_dir)):
        os.makedirs(output_image_dir)

    with open(os.path.join(output_dir, 'split_result', coco_class), mode='r', encoding='utf-8') as f:
        image_list =f.readlines()
    edd = X2COCO(categories, category_list)

    for i in image_list:
        i = i.replace('\n', '')
        path, filename = os.path.split(i)

        edd.add_image(path, filename, output_image_dir)

        bbox = df.loc[df['filename']==filename, ['x1', 'y1', 'x3', 'y3', 'finding_class']].values[0]
        edd.generate_anno_field(
            [bbox[0], bbox[1], bbox[2]-bbox[0], bbox[3]-bbox[1]], bbox[4]
        )
    edd.save_json(os.path.join(output_dir, 'annotations', 'instances_'+coco_class+'2017.json'))
    categories = edd.categories
    category_list = edd.categories_list

edd.save_labels(os.path.join(output_dir, 'labels.txt'))
