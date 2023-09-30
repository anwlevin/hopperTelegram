#!/usr/bin/env python

import pathlib

import telegram
import yaml

from config import STORE
from message_saver import message_text_filter
from utils import read_file, write_file


def getIndexOnePost(data: dict):

    message = None
    text_md = None
    if hasattr(data, 'message'):
        message = data.get('message')
        text_md = data.get('markdown_text')
    else:
        message = data
        text_md = message.get('text')

    print()
    print('TEXT', text_md)
    print()

    text = ''
    text += f'### post-{message.message_id}'
    text += '\n'
    text += '\n'
    text += f'{message.date.__str__()}'
    text += '\n'
    text += '\n'
    text += text_md
    text += '\n'

    return text


def indexChat(chat):
    print(chat)
    text = '\n'

    files = chat.iterdir()
    files = sorted(list(filter(lambda file: not file.name.startswith('index'), files)), reverse=True)
    for post in files:
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

    files = store.iterdir()
    files = sorted(list(filter(lambda file: not file.name.startswith('index'), files)), reverse=True)
    for chat in files:
        indexChat(chat)


if __name__ == '__main__':
    indexAllChats()
