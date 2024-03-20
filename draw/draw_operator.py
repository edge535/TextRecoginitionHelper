from PIL.ImageFont import FreeTypeFont
from PIL import Image, ImageDraw


def paint(
        content: str,
        background: Image,
        font: FreeTypeFont,
        position: tuple[int, int],
        color: tuple = (0, 0, 0),
        anchor: str = 'lt'
):
    draw = ImageDraw.Draw(background)
    draw.text(position, content, font=font, fill=color, anchor=anchor)
    return background


def get_relative_position_in_image(font_width: int, font_height: int,
                                   image_x: int, image_y: int,
                                   offset_x: int = 0, offset_y: int = 0) -> tuple[int, int]:
    position_x = ((image_x - font_width) // 2) + offset_x
    position_y = ((image_y - font_height) // 2) + offset_y

    return position_x, position_y
