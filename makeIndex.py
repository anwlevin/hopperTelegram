#!/usr/bin/env python

import pathlib

import telegram
import yaml

from config import STORE
from message_saver import message_text_filter
from utils import read_file, write_file


def getIndexOnePost(yaml: dict):
    message = yaml['message']

    text = ''
    text += f'### post-{message.message_id}'
    text += '\n'
    text += '\n'
    text += f'{message.date.__str__()}'
    text += '\n'
    text += yaml['markdown_text']
    text += '\n'

    return text


def indexChat(chat):
    print(chat)
    text = '\n'
    for post in sorted(chat.iterdir(), reverse=True):
        if not post.name.startswith('post-'):
            continue

        yaml_text = read_file(post)
        yaml_data = yaml.load(yaml_text, Loader=yaml.Loader)
        text += getIndexOnePost(yaml_data)
        text += '\n'
        text += '\n'
        text += '\n'

    index = chat.joinpath('index.md')
    write_file(index, text)


def indexAllChats():
    print('💎️', 'Make Index')
    store = pathlib.Path(STORE)

    for chat in store.iterdir():
        indexChat(chat)


if __name__ == '__main__':
    indexAllChats()
