import argparse
import os
from draw.job import Job

current_path = os.path.split(os.path.realpath(__file__))[0]


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="一个用于文本识别时样本生成的工具"
    )

    parser.add_argument(
        '-out',
        '--output',
        type=str,
        help='生成样本保存位置',
        default=os.path.join(current_path, 'output')
    )

    parser.add_argument(
        '-back',
        '--background',
        type=str,
        help='指定背景图片地址',
        default=os.path.join(current_path, 'background')
    )

    parser.add_argument(
        '-content',
        '--content',
        type=str,
        help='指定内容文本地址',
        default=os.path.join(current_path, 'content')
    )

    parser.add_argument(
        '-font',
        '--font',
        type=str,
        help='指定字体地址',
        default=os.path.join(current_path, 'font')
    )

    parser.add_argument(
        '-num',
        '--sample_num',
        type=int,
        help='生成的样本个数',
        default=1
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    os.makedirs(args.output, exist_ok=True)
    res = Job(args.background, args.font, args.content, args.sample_num).get_result()
    i = 1
    for r in res:
        r.save(os.path.join(args.output, f'{i}.png'))
        i += 1
