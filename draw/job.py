import os

from background.background_operator import get_images_by_direct, get_a_background_image, get_image_size
from draw.draw_operator import paint, get_relative_position_in_image
from font.font_operator import get_fonts_by_direct, get_suitable_font_size, get_content_real_size, get_a_font
from content.content_operator import get_contents_by_direct, get_contents_in_file


def relative_2_absolute(relative_path):
    return os.path.abspath(relative_path)


def resize_list(now_list: list[str], need_num: int) -> list[str]:
    if need_num > len(now_list):
        now_list = now_list * (need_num // len(now_list)) + \
                   now_list[:need_num % len(now_list)]
    else:
        now_list = now_list[:need_num]
    return now_list


def check_background_param(background_param):
    background_param = relative_2_absolute(background_param)
    if os.path.isfile(background_param):
        return [background_param]
    elif os.path.isdir(background_param):
        return get_images_by_direct(background_param)
    else:
        raise ValueError('路径无权访问或者不存在')


def check_font_param(font_param):
    font_param = relative_2_absolute(font_param)
    if os.path.isfile(font_param):
        return [font_param]
    elif os.path.isdir(font_param):
        return get_fonts_by_direct(font_param)
    else:
        raise ValueError('路径无权访问或者不存在')


def check_content_param(content_param):
    content_param = relative_2_absolute(content_param)
    if os.path.isfile(content_param):
        return get_contents_in_file(content_param)
    elif os.path.isdir(content_param):
        return get_contents_by_direct(content_param)
    else:
        raise ValueError('路径无权访问或者不存在')


class Job:
    def __init__(self,
                 background_path: str,
                 font_path: str,
                 content_path: str,

                 sample_num: int,

                 font_size: tuple[int, int] | int | str = 'suitable',
                 position: tuple[int, int] | str = 'middle',
                 ):
        self.font_size = font_size
        self.position = position

        self.background: list[str] = resize_list(check_background_param(background_path), sample_num)
        self.font: list[str] = resize_list(check_font_param(font_path), sample_num)
        self.content: list[str] = resize_list(check_content_param(content_path), sample_num)
        self.task: list[tuple[str, str, str]] = zip(self.background, self.font, self.content)

    def get_task(self):
        return self.task

    def get_result(self):
        result = []
        for back, font, content, in self.task:
            _font_size = None
            _position = None

            image = get_a_background_image(back)
            image_w, image_h = get_image_size(image)

            if isinstance(self.font_size, str):
                if self.font_size == 'suitable':
                    _font_size = get_suitable_font_size(content, font, (image_w, image_h))
            elif isinstance(self.font_size, int):
                _font_size = self.font_size
            elif isinstance(self.font_size, tuple):
                _font_size = get_suitable_font_size(content, font, (image_w, image_h),
                                                    font_size_range=(self.font_size[0], self.font_size[1]))
            else:
                raise ValueError('font size 无法处理')

            _font = get_a_font(font, _font_size)
            font_w, font_h, _ = get_content_real_size(content, _font)

            if isinstance(self.position, str):
                if self.position == 'middle':
                    _position = get_relative_position_in_image(font_w, font_h, image_w, image_h)
            elif isinstance(self.position, tuple):
                _position = (self.position[0], self.position[1])
            else:
                raise ValueError('position 无法处理')

            drew = paint(content, image, _font, _position)
            result.append(drew)

        return result


if __name__ == '__main__':
    job = Job(
        background_path='../background/data',
        font_path='../font/data',
        content_path='../content/data',
        sample_num=10,
    )
    a = job.get_result()
    for i in a:
        i.show()
