import os
import random


def get_contents_in_file(path: str) -> list[str]:
    contents = []
    with open(path, 'r') as f:
        contents = [line for line in f.read().splitlines() if len(line) > 0]
    return contents


def get_contents_by_direct(content_direct: str, shuffle: bool = True) -> list[str]:
    contents_list: list[str] = []
    for pre_path, _, contents, in os.walk(content_direct):
        for content in contents:
            if content.lower().endswith(".txt"):
                content_path = os.path.join(pre_path, content)
                lines = get_contents_in_file(content_path)
                contents_list.extend(lines)
    if shuffle:
        random.shuffle(contents_list)
    return contents_list
