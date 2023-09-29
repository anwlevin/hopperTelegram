#!/usr/bin/env python

import pathlib

import telegram
import yaml

from config import STORE
from message_saver import message_text_filter
from utils import read_file, write_file


def getIndexOnePost(message: telegram.Message):
    text = ''

    text += f'### post-{message.message_id}'
    text += '\n'
    text += '\n'
    text += f'{message.date.__str__()}'
    text += '\n'
    text += f'{message_text_filter(message.text_markdown_v2.__str__())}'
    text += '\n'

    return text



def indexChat(chat):
    print(chat)
    text = '\n'
    for post in sorted(chat.iterdir(), reverse=True):
        if not post.name.startswith('post-'):
            continue

        yml = read_file(post)
        message = yaml.load(yml, Loader=yaml.Loader)
        text += getIndexOnePost(message)
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
