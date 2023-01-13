import os
import shutil
import json
from tqdm import tqdm
from tools import *
from utils import is_pic, get_encoding

# planthopper_2417数据集目录结构处理
origin_path = 'datasets/pests/planthopper_2417_origin'
saved_path = 'datasets/pests/planthopper_2417'
if not os.path.exists(saved_path):
    os.makedirs(saved_path)
    
    for dir in os.listdir(origin_path):
        dir_name = os.path.join(origin_path, dir)
        for file in os.listdir(dir_name):
            if file.split('.')[1] == 'txt':
                shutil.copy(os.path.join(dir_name, file), os.path.join(saved_path, file))
            else:
                shutil.copy(os.path.join(dir_name, file), os.path.join(saved_path, file.split('.')[0]+'.jpg'))

imageDirs = ['datasets/pests/aphid', 'datasets/pests/mspider', 'datasets/pests/planthopper_135', 'datasets/pests/planthopper_2417']
output_dir = 'output/pests_yolo/'
if not(os.path.exists(os.path.join(output_dir, 'split_result'))):
    images_list = []
    for path in imageDirs:
        for filename in os.listdir(path):
            if is_pic(filename):
                images_list.append(os.path.join(path, filename))

    dataset_split(images_list, train=0.5, val=0.2, test=0.3, outputDir=output_dir, mode=1)

coco_annotations = os.listdir(os.path.join(output_dir, 'split_result'))
categories=[]
for coco_class in coco_annotations:
    output_image_dir = os.path.join(output_dir, coco_class)
    if not(os.path.exists(output_image_dir)):
        os.makedirs(output_image_dir)

    with open(os.path.join(output_dir, 'split_result', coco_class), mode='r', encoding='utf-8') as f:
        image_list =f.readlines()
    transObject = X2YOLO(categories)

    print('开始处理'+coco_class)
    for i in tqdm(image_list):
        i = i.replace('\n', '')
        path, filename = os.path.split(i)

        w, h, new_img_path = transObject.add_image(path, filename, output_image_dir)

        if '2417' in path:
            anno_origin_file = os.path.splitext(i)[0]+'.txt'
        else:
            anno_origin_file = os.path.splitext(i)[0]+'.json'
        
        with open(anno_origin_file, mode='r', \
            encoding=get_encoding(anno_origin_file)) as j:
            json_info = json.load(j)
        
        bboxs = []
        if '2417' in path:
            for region in json_info['regions']:
                regionOrigin = region['region']
                bboxs.append([regionOrigin[0], regionOrigin[1], regionOrigin[2]-regionOrigin[0], regionOrigin[3]-regionOrigin[1], 'planthopper'])
        else:
            for region in json_info['labels']:
                if '135' in path:
                    bboxs.append([region['x1'], region['y1'], region['x2']-region['x1'], region['y2']-region['y1'], 'planthopper'])
                else:
                    bboxs.append([region['x1'], region['y1'], region['x2']-region['x1'], region['y2']-region['y1'], region['name']])
        
        transObject.generate_anno_field(bboxs, w, h, os.path.splitext(new_img_path)[0]+'.txt')
    categories = transObject.categories

transObject.save_labels(os.path.join(output_dir, 'labels.txt'))
