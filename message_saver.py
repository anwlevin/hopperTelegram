#!/usr/bin/env python

import pathlib
from os import getcwd
from pathlib import Path
import re
import yaml
from slugify import slugify
from telegram import Message

from config import STORE
from utils import write_file

WHERE_ALL_STORES = 'storeTelegramChats'
DEBUG = True
DEBUG_SAVE_RAW_DATA = True


def chat_title_clean(title: str = '', pattern: str = 'U(u*)-u'):
    """
    Return all parts of remain after cutting Uuuuuu-uu
    (1)(Uuuuu-u)(2)
    :param pattern:
    :param title:
    :return:
    """
    res = re.search(pattern, title)
    if not res:
        return slugify(title)

    parts = [slugify(title[:res.span()[0]]), slugify(title[res.span()[1]:])]

    return parts


def get_dynamic_filename(
        prefix: str = '',
        dynamic_text: str = '',
        suffix: str = '',
        max_length: int = 16) -> str:
    """

    :param prefix:
    :param dynamic_text:
    :param suffix:
    :param max_length:
    :return:
    """
    words = slugify(dynamic_text).split('-')
    small_name = ''

    local_max_length = max_length - len(prefix) - len(suffix)
    for index in range(len(words)):
        if index == 0:
            if len(words[index]) > local_max_length:
                small_name = words[index][:local_max_length]
                break
            else:
                small_name = words[index]
                continue

        proposed_name = f'{small_name}-{words[index]}'
        if len(proposed_name) > local_max_length:
            break

        small_name = proposed_name

    return f'{prefix}{small_name}{suffix}'


def chat_id_sanitize(
        chat_id_original: str,
        prefix_chat_id_to_remove: str = '-100') -> str:

    """

    :param chat_id_original:
    :param prefix_chatid_to_remove:
    :return:
    """
    if not chat_id_original.startswith("-"):
        return chat_id_original

    if chat_id_original.startswith(prefix_chat_id_to_remove):
        return chat_id_original.removeprefix(prefix_chat_id_to_remove)

    return chat_id_original


def message_text_filter(text: str = '') -> str:
    """

    :param text:
    :return:
    """
    text = text.replace("\\", "")
    text = f'\n{text}\n'

    return text


def MessageSaverTELCON2(message: Message, update_id: str):
    print('\n\n', 'Message: ', message)
    print('🍎', message.chat.id)
    chat_id = chat_id_sanitize(message.chat.id.__str__())
    chat_title = chat_title_clean(message.chat.title)

    #chat_dirname = get_dynamic_filename(
    #    f'chat-{chat_id}-',
    #    f'{chat_title}',
    #    f'',
    #)

    chat_dirname = f'chat-{chat_id}-{chat_title}'

    store = pathlib.Path(STORE)

    chat = store.joinpath(chat_dirname)
    chat.mkdir(parents=True, exist_ok=True)

    post = chat.joinpath(f'post-{message.message_id}.yml')

    context = dict()
    context['message'] = message

    context['markdown_text'] = message_text_filter(message.text_markdown_v2.__str__())

    text = yaml.dump(
        context,
        default_flow_style=False,
        sort_keys=False,
        allow_unicode=True,
    )

    write_file(post, text)


    return

    context['post'] = text
    context['date'] = update.channel_post.date.__str__()
    context['chat_title'] = update.channel_post.chat.title.__str__()
    context['chat_id'] = update.channel_post.chat.id.__str__()
    context['message_id'] = update.channel_post.message_id.__str__()
    context['chat_type'] = update.channel_post.chat.type.__str__()

    if DEBUG_SAVE_RAW_DATA:
        context['rawdata'] = update

    dir_chat_name = get_dynamic_filename(
        f'{chat_id_sanitize(update.channel_post.chat.id.__str__())}-',
        f'{chat_title_clean(update.channel_post.chat.title.__str__()).__str__()}',
        f'-chat',
    )
    full_dir_chat_name = '/'.join([getcwd(), WHERE_ALL_STORES, dir_chat_name])
    Path(full_dir_chat_name).mkdir(parents=True, exist_ok=True)

    file_name = get_dynamic_filename(
        f'{update.channel_post.message_id}-',
        f'{update.channel_post.text}',
        f'.txt',
    )

    full_path = '/'.join([full_dir_chat_name, file_name])
    print('full_path: ', full_path)

    with open(full_path, 'w') as f:
        yaml.dump(
            context,
            f,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )



