"""
修改图片像素
"""
from PIL import Image

def change_black_to_dark_blue(image_path, output_path):
    """将图像中的黑色像素改为深蓝色"""
    # 打开图像
    img = Image.open(image_path)
    # 将图像转换为 RGBA 模式,以确保有 alpha 通道
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    # 加载图像的数据
    pixels = img.load()

    # 获取图像的宽度和高度
    width, height = img.size

    # 遍历图像中的每个像素
    for x in range(width):
        for y in range(height):
            # 检查像素值是否为黑色且有透明度为255
            if pixels[x, y] == (0, 0, 0, 255):  # 假设不透明像素的 alpha 值为 255
                # 将黑色像素改为深蓝色 (0, 0, 1)
                pixels[x, y] = (0, 0, 1, 255)

    # 保存修改后的图像
    img.save(output_path)

# 使用示例
change_black_to_dark_blue("/Users/chenjianxu/PycharmProjects/pythonProject/SUPER_MARIO/resources/graphics/enemies.png", "/Users/chenjianxu/PycharmProjects/pythonProject/SUPER_MARIO/resources/graphics/enemies1.png")