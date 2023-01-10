import os
from tools import *

imageDirs = ['datasets/EDD/images']
output_dir = 'output/EDD/'
if not(os.path.exists(os.path.join(output_dir, 'split_result'))):
    dataset_split(imageDirs, train=0.5, val=0.2, test=0.3, outputDir=output_dir)
if not(os.path.exists(os.path.join(output_dir, 'annotations'))):
    os.makedirs(os.path.join(output_dir, 'annotations'))

coco_annotations = ['train', 'test', 'val']
categories=[]
category_list=[]
for coco_class in coco_annotations:
    output_image_dir = os.path.join(output_dir, 'images', coco_class+'2017')
    if not(os.path.exists(output_image_dir)):
        os.makedirs(output_image_dir)

    with open(os.path.join(output_dir, 'split_result', coco_class+'.txt'), mode='r', encoding='utf-8') as f:
        image_list =f.readlines()
    edd = X2COCO(categories, category_list)

    for i in image_list:
        i = i.replace('\n', '')
        path, filename = os.path.split(i)

        edd.add_image(path, filename, output_image_dir)

        anno_path = path.replace('images', 'bbox')
        anno_filename = filename.split('.')[0] + '.txt'

        with open(os.path.join(anno_path, anno_filename), 'r') as f:
            bboxs = f.readlines()
        for bbox in bboxs:
            x, y, width, height, label = bbox.split(' ')
            edd.generate_anno_field(
                [float(x), float(y), float(width), float(height)], label.replace('\n', '')
            )
    edd.save_json(os.path.join(output_dir, 'annotations', 'instances_'+coco_class+'2017.json'))
    categories = edd.categories
    category_list = edd.categories_list

edd.save_labels(os.path.join(output_dir, 'labels.txt'))
