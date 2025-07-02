import random
import matplotlib.pyplot as plt

# 1. 从CSV文件中读取数据
def read_csv(file_path):
    content = []

    """
    在这里撰写读取csv文件的代码，输出content形状为
    content = [ (image-1.data(2D), image-1.label), (image-2.data(2D), image-2.label) ...]
    """

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
csv_file = 'mnist_test.csv'

# 读取 CSV 数据
content = read_csv(csv_file)

# 随机选择并可视化一个图像
visualize_random_image(content)
