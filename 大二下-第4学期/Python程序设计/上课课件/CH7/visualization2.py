import random
import matplotlib.pyplot as plt

# 1. 从CSV文件中读取数据
def read_csv(file_path):
    content = []
    with open(file_path, 'r') as f:
        lines = f.readlines()  # 读取所有行
        for line in lines:
            # 以逗号分割每一行，得到每个像素点和标签
            row = line.strip().split(',')
            # 将前784个像素值转换为28x28的二维list
            image = [list(map(int, row[i:i+28])) for i in range(0, 784, 28)]
            label = int(row[784])  # 标签是最后一位
            content.append((image, label))
    return content

# 2. 随机选择一个元素并进行可视化
def visualize_random_image(content):
    # 随机选择一个元素
    random_data = random.choice(content)
    image, label = random_data
    
    # 可视化该图片
    plt.imshow(image, cmap='gray')  # 使用灰度色图
    plt.title(f"Label: {label}")  # 在图片上显示标签
    plt.axis('off')  # 关闭坐标轴
    plt.show()

# 设置 CSV 文件路径
csv_file = 'F:/Upan/课件/大二下/Python程序设计/CH7/mnist_test.csv'

# 读取 CSV 数据
content = read_csv(csv_file)

# 随机选择并可视化一个图像
visualize_random_image(content)
