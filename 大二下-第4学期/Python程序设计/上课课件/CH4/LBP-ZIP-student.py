from PIL import Image
import matplotlib.pyplot as plt

# 图像转二维列表
def image_to_gray_array(img):
    width, height = img.size
    pixels = img.load()
    return [[pixels[x, y] for x in range(width)] for y in range(height)]

# 二维列表转图像
def array_to_image(array):
    height = len(array)
    width = len(array[0])
    img = Image.new('L', (width, height))
    for y in range(height):
        for x in range(width):
            img.putpixel((x, y), array[y][x])
    return img

# 使用 本节课学过的知识计算LBP值
def get_lbp_value(center, neighbors):
    lbp_score = 0
    li = list(map(lambda x: 1 if x > center else 0, neighbors))
    for i in range(len(li)):
        lbp_score =lbp_score + li[i] * 2 **(7-i)
    return lbp_score

def calculate_lbp(image_array, visualize=False, delay=0.01):
    height = len(image_array)
    width = len(image_array[0])
    result = [[0] * width for _ in range(height)]

    if visualize:
        plt.ion()
        fig, ax = plt.subplots()
        img_plot = ax.imshow(result, cmap='gray', vmin=0, vmax=255)
        plt.title("LBP - Internal Only")
        plt.axis('off')

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            center = image_array[i][j]
            neighbors = [
                image_array[i-1][j-1], image_array[i-1][j], image_array[i-1][j+1],
                image_array[i][j+1],   image_array[i+1][j+1], image_array[i+1][j],
                image_array[i+1][j-1], image_array[i][j-1]
            ]
            result[i][j] = get_lbp_value(center, neighbors)

        if visualize and i % 5 == 0:
            img_plot.set_data(result)
            plt.pause(delay)

    if visualize:
        plt.ioff()
        plt.show()

    return result


def main():
    img_path = 'C:/Users/1/Desktop/tiger.jpg'
    gray_img = Image.open(img_path).convert('L')
    gray_array = image_to_gray_array(gray_img)

    lbp_array = calculate_lbp(gray_array, visualize=True, delay=0.02)
    lbp_img = array_to_image(lbp_array)
    lbp_img.save('lbp_internal_only.png')
    print("LBP计算完成，已保存为 lbp_internal_only.png")

if __name__ == '__main__':
    main()
