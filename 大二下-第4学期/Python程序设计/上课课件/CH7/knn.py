import random
import math
import matplotlib.pyplot as plt
from collections import Counter
from tqdm import tqdm  # 导入 tqdm 库

# 1. 从CSV文件中读取10000条数据
def read_csv(file_path, n_samples=10000):
    content = []
    with open(file_path, 'r') as f:
        lines = f.readlines()  # 读取所有行
        print(f"读取数据中，目标读取 {n_samples} 条数据...")
        for i, line in enumerate(tqdm(lines[:n_samples], desc="读取数据进度", unit="条")):
            row = line.strip().split(',')
            image = list(map(int, row[:784]))  # 将前784个像素值保存为一维list
            label = int(row[784])  # 标签是最后一位
            content.append((image, label))
    return content

# 2. 随机打乱数据并按8:2划分训练集和测试集
def split_data(content, train_ratio=0.8):
    print("正在随机打乱数据并划分训练集和测试集...")
    random.shuffle(content)  # 打乱数据
    
    return train_data, test_data

# 3. 计算两点之间的欧几里得距离
def euclidean_distance(img1, img2):

    return 

# 4. KNN分类
def knn_classify(train_data, test_img, k=3):
    distances = []
    # 计算当前样本到训练集中所有样本的距离，并加入到distances数组中
    
    
    # 按照距离排序，选择最近的k个邻居
    
    
    # 投票决定最终的预测标签
    
    return final_label

# 5. 计算预测准确率
def calculate_accuracy(train_data, test_data, k=3):
    correct_predictions = 0
    print(f"正在进行测试集的预测，测试集大小: {len(test_data)}...")
    # 计算test数据集上所有样本的准确率，即预测label与实际label相同的样本占总样本个数的比值

    return accuracy

# 设置文件路径
csv_file = 'mnist_test.csv'

# 1. 从CSV文件中读取数据
content = read_csv(csv_file, n_samples = 10000)

# 2. 划分训练集和测试集
train_data, test_data = split_data(content)

# 3. 计算测试集的准确率
accuracy = calculate_accuracy(train_data, test_data, k=3)

print(f"预测准确率: {accuracy:.2f}%")
