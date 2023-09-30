#!/usr/bin/env python

import pathlib
from config import STORE
from utils import read_file, write_file



def indexDir(current_dir):
    print('💎️', 'Make index Dir')
    files = current_dir.iterdir()
    files = list(filter(lambda file: not file.name.startswith('index'), files))

    text = '\n'
    text += f'# Index of {current_dir}'
    text += '\n'
    text += '\n'

    for file in files:
        print(file)
        text += f' - ## [{file.relative_to(current_dir)}]({file.as_posix()}/)'
        text += '\n'
        text += '\n'

    text += '\n'
    text += '\n'

    index = current_dir.joinpath('index.md')
    write_file(index, text)


if __name__ == '__main__':
    store = pathlib.Path(STORE)
    indexDir(store)
