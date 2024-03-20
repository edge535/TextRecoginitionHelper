import os
import random

from PIL import ImageFont
from PIL.ImageFont import FreeTypeFont


def get_a_font(font_path: str, font_size: int = 10) -> FreeTypeFont:
    """
    以指定路径、指定字体大小加载一个字体
    :param font_path: 路径
    :param font_size: 大小
    :return: 字体
    """
    font = ImageFont.truetype(font_path, font_size)
    return font


def get_fonts_by_direct(fonts_direct: str, shuffle: bool = True) -> list[str]:
    fonts: list[str] = []
    for pre_path, _, contents, in os.walk(fonts_direct):
        for content in contents:
            if content.lower().endswith(".ttf"):
                content_path = os.path.join(pre_path, content)
                fonts.append(content_path)
    if shuffle:
        random.shuffle(fonts)
    return fonts


def get_content_real_size(content: str, font: FreeTypeFont) -> tuple[int, int, int]:
    """
    计算给定文本在 指定字体 指定大小下 的尺寸
    :param content: 文本内容
    :param font: 字体
    :return: 文本宽度，文本高度，文本上填充
    """
    font_left, font_top, font_right, font_bottom = font.getbbox(content)

    font_width = font_right - font_left
    font_height = font_bottom - font_top

    return font_width, font_height, font_top


def get_suitable_font_size(content: str,
                           font_path: str,
                           image_size: tuple[int, int],
                           display_range: tuple[float, float] | float = 0.9,
                           min_boundary: bool = True,
                           font_size_range: tuple[int, int] = (5, 100)
                           ) -> int:
    """
    计算在给定图片上、以给定的字体显示内容时，不超过显示范围的最大字体尺寸
    :param content: 文本内容
    :param font_path: 字体路径
    :param image_size: 图片宽高
    :param display_range: 图片上可用于显示内容的比例
    :param min_boundary: 内容严格限制在图片的范围内、若未False时，可能会出现宽或高超出图片范围
    :param font_size_range: 字体尺寸的参考范围
    :return: 合适的字体尺寸
    """
    display_range_factor = (display_range, display_range) if isinstance(display_range, float) else display_range
    image_width = image_size[0] * display_range_factor[0]
    image_height = image_size[1] * display_range_factor[1]
    suitable_size = font_size_range[1]
    for size in range(font_size_range[0], font_size_range[1] + 1):
        font = get_a_font(font_path, size)
        content_width, content_height, _ = get_content_real_size(content, font)
        over_width = content_width > image_width
        over_height = content_height > image_height
        if min_boundary and (over_width or over_height):
            suitable_size = size - 1
            break
        elif not min_boundary and (over_width and over_height):
            suitable_size = size - 1
            break
    return suitable_size
