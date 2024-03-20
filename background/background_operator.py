import os
import random

from PIL import Image


def is_image_file(file_path: str) -> bool:
    """
    判断一个文件是否是可以打开的图片
    :param file_path: 文件路径
    :return: 是否
    """
    _, ext = os.path.splitext(file_path)
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    if ext.lower() in image_extensions:
        try:
            Image.open(file_path)
            return True
        except Exception as _:
            return False
    else:
        return False


def get_image_size(image: Image) -> tuple[int, int]:
    """
    图片的尺寸
    :param image: 图片
    :return: 宽,高
    """
    return image.size


def get_a_background_image(image_path: str) -> Image:
    """
    读取一个图片
    :param image_path: 图片路径
    :return: 图片
    """
    background_image = Image.open(image_path)
    return background_image


def get_images_by_direct(images_direct: str, shuffle: bool = True) -> list[str]:
    """
    加载一个给定路径下的所有可打开的图片文件，随机打乱顺序
    :param images_direct: 指定文件夹
    :param shuffle: 是否被打乱
    :return: 图片集
    """
    images: list[str] = []
    for pre_path, _, contents, in os.walk(images_direct):
        for content in contents:
            content_path = os.path.join(pre_path, content)
            if is_image_file(content_path):
                images.append(content_path)
    if shuffle:
        random.shuffle(images)
    return images
