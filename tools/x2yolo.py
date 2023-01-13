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
import os

class X2YOLO(object):
    def __init__(self, categories=[]):
        # 中间变量
        self.image_id = 0
        self.categories = categories

        # 结果生成用
        self.annotations_list = []
    
    # def get_image_size(self, image_path, filename):
    #     """
    #     获取图像尺寸
    #     Output:
    #         [width, height]
    #     """
    #     img = cv2.imread(os.path.join(image_path, filename))
    #     return [img.shape[1], img.shape[0]]
    
    def generate_anno_with_first_point(self, bboxs, width, height):
        """
        用第一个点生成anno_field
        Args：
            bbox: [x, y, width, height, label]
        """
        # print(bboxs)
        for bbox in bboxs:
            x = bbox[0]+bbox[2]/2
            y = bbox[1]+bbox[3]/2
            w = bbox[2]
            h = bbox[3]
            
            self.annotations_list.append('{} {} {} {} {}'.format(self.get_category_id(bbox[4]), x/width, y/height, w/width, h/height))
        
    def generate_anno_with_centre_point(self, bboxs, width, height):
        """
        用第一个点生成anno_field
        Args：
            bbox: [x, y, width, height, label]
        """
        for bbox in bboxs:
            x = bbox[0]
            y = bbox[1]
            w = bbox[2]
            h = bbox[3]
            self.annotations_list.append('{} {} {} {} {}'.format(self.get_category_id(bbox[4]), x/width, y/height, w/width, h/height))

    def generate_anno_field(self, bboxs, width, height, output_file_path, mode=0):
        self.annotations_list = []
        if mode == 0: # 用第一个点生成anno field
            self.generate_anno_with_first_point(bboxs, width, height)
        else: # 用中心点生成anno field
            self.generate_anno_with_centre_point(bboxs, width, height)

        self.save_anno(output_file_path)

    def get_category_id(self, label):
        if label in self.categories: 
            return self.categories.index(label)
        self.categories.append(label)
        return len(self.categories)-1

    def add_image(self, image_path, filename, output_path):
        """
        添加图片
        Args:
            image_path (str)：路径名（不含文件名）
            filename (str)：文件名
            output_path (str): 图片保存路径（不含文件名）
        Output:
            [width, height, new_file_path]
        """
        self.image_id += 1
        new_filename = "{}{}".format(self.image_id, os.path.splitext(filename)[1])
        
        img = cv2.imread(os.path.join(image_path, filename))
        
        cv2.imwrite(os.path.join(output_path, new_filename), img)
        return [img.shape[1], img.shape[0], os.path.join(output_path, new_filename)]

    def save_anno(self, output_file):
        with open(output_file, 'w') as f:
            f.writelines('\n'.join(self.annotations_list))
    
    def save_labels(self, output_file):
        with open(output_file, 'w') as f:
            f.writelines('\n'.join(self.categories))
    