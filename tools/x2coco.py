# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cv2
import json
import os
import shutil

class X2COCO(object):
    def __init__(self, categories=[], category_list=[]):
        # 中间变量
        self.categories = categories
        self.image_id = 0
        self.anno_id = 0

        # 结果生成用
        self.images_list = []
        self.categories_list = category_list
        self.annotations_list = []
    
    # def generate_image_field(self, image_path, filename):
    #     self.image_id += 1
    #     image = {} 
    #     image["id"] = self.image_id
    #     image['file_name'] = filename
    #     img = cv2.imread(os.path.join(image_path, filename))
    #     image["height"] = img.shape[0]
    #     image["width"] = img.shape[1]
        
    #     return image
    
    def generate_category_field(self, label):
        category = {}
        category["id"] = len(self.categories)
        category["supercategory"] = "component"
        category["name"] = label
        
        return category
    
    def generate_anno_field(self, bbox, label, segmentation=[], iscrowd=0):
        self.anno_id += 1
        self.annotations_list.append({
            "id": self.anno_id,
            "image_id": self.image_id,
            "category_id": self.get_category_id(label),
            "bbox": bbox,
            "area": bbox[2]*bbox[3],
            "segmentation": segmentation,
            "iscrowd": iscrowd
        })

    def get_category_id(self, label):
        if label in self.categories: 
            return self.categories.index(label)+1
        self.categories.append(label)
        self.categories_list.append(self.generate_category_field(label))
        return len(self.categories)

    def add_image(self, image_path, filename, output_path):
        """
        添加图片
        Args:
            image_path (str)：路径名（不含文件名）
            filename (str)：文件名
            output_path (str): 图片输出保存路径名
        """
        self.image_id += 1
        
        image = {} 
        image["id"] = self.image_id
        image['file_name'] = "{}{}".format(self.image_id, os.path.splitext(filename)[1])
        
        img = cv2.imread(os.path.join(image_path, filename))
        image["height"] = img.shape[0]
        image["width"] = img.shape[1]
        
        cv2.imwrite(os.path.join(output_path, image['file_name']), img)
        self.images_list.append(image)

    def save_json(self, output_file):
        coco_data = {
            "images": self.images_list,
            "categories": self.categories_list,
            "annotations": self.annotations_list
        }
            
        with open(output_file, 'w') as f:
            json.dump(coco_data, f, indent=4)
    
    def save_labels(self, output_file):
        with open(output_file, 'w') as f:
            f.writelines('\n'.join(self.categories))