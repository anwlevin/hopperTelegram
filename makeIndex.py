#!/usr/bin/env python

import pathlib

import telegram
import yaml

from config import STORE
from message_saver import message_text_filter
from utils import read_file, write_file


def getIndexOnePost(message: telegram.Message, data: dict):
    text = ''
    text += f'### post-{message.message_id}'
    text += '\n'
    text += '\n'
    text += f'{message.date.__str__()}'
    text += '\n'
    text += '\n'
    text += data.get('text_html')
    text += '\n'
    text += '\n'

    return text


def indexChat(chat):
    print(chat)
    text = '\n'

    files = chat.iterdir()
    files = sorted(list(filter(lambda file: not file.name.startswith('index'), files)), reverse=True)
    for post in files:
        text_post = read_file(post)
        yaml_post = yaml.load(text_post, Loader=yaml.Loader)

        message_post = yaml_post.get('message')
        data_post = yaml_post.get('data')
        text += getIndexOnePost(message_post, data_post)
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
