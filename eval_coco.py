# import os
# import json
# import cv2
# from tqdm import tqdm

# coco_file_path = 'output/pests_coco/annotations/instances_train2017.json'
# image_dir_path = 'output/pests_coco/images/train2017'
# output_file = 'record.txt'

# with open(coco_file_path, 'r') as f:
#     coco = json.load(f)

# record = []
# for image in tqdm(coco['images']):
#     image_path = os.path.join(image_dir_path, image['file_name'])
#     img = cv2.imread(image_path)
#     if image['height'] != img.shape[0]:
#         record.append('The actual height of {} is {}, but {} is saved in the dataset'.format(image['file_name'], img.shape[0], image['height']))
#     if image['width'] != img.shape[1]:
#         record.append('The actual width of {} is {}, but {} is saved in the dataset'.format(image['file_name'], img.shape[1], image['width']))

# with open(output_file, 'w') as f:
#     f.write('{}\n'.format(len(record)))
#     f.writelines('\n'.join(record))


import cv2

img = cv2.imread('output/pests_coco/images/test2017/376.jpg')
print(img.shape[0])