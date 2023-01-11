import os
from sklearn.model_selection import train_test_split

def split(list, train, val, test, random_state=None):
    """
    split the dataset
    """
    if train == 1:
        return list
    # if train + val + test != 1 or train == 0:
    #     raise Exception('检查数据集划分参数')
    
    train_path, test_path = train_test_split(list, train_size=train, random_state=random_state)
    if val == 0:
        return [train_path, test_path]
    val_path, test_path = train_test_split(test_path, train_size=val/(val+test), random_state=random_state)
    return [train_path, test_path, val_path]

def save_split_result(outputDir, dataset):
    """
    save the split result
    """ 
    saved_path = os.path.join(outputDir, 'split_result')
    if not os.path.exists(saved_path):
            os.makedirs(saved_path)
    text = ['train', 'test', 'val']
    for i in range(len(dataset)):
        with open(os.path.join(saved_path, text[i]), encoding='utf-8', mode='w+') as f:
            f.writelines('\n'.join(dataset[i]))

def dataset_split(paths, train, val, test, random_state=None, outputDir='', mode=0):
    """
    划分数据集

    Args:
        list ([str]): 待分文件路径列表
        train, val, test(float): 划分比例，训练集、验证集、测试集，和需为1，验证集可为0
        random_state：随机种子，用于复现
        mode(int): 若mode为0，paths为文件夹名，否则paths为文件名
    Output：
        train=1: train_list
        train<1 and val=0: [train_list, test_list]
        train<1 and val>0: [train_list, test_list, val_list]
    """
    pathList = []
    if mode == 0:
        for path in paths:
            for filename in os.listdir(path):
                pathList.append(os.path.join(path, filename))
    else:
        pathList = paths
    
    dataset = split(pathList, train, val, test, random_state)
    if outputDir == '':
        return dataset
    else:
        save_split_result(outputDir, dataset)