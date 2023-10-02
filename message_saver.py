#!/usr/bin/env python

import pathlib
from os import getcwd
from pathlib import Path
import re
import yaml
from slugify import slugify
from telegram import Message
from telegram.ext import ContextTypes

import config
from config import CHATS_STORE
from utils import write_file, read_file

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

    text = text.replace("\\", "")
    text = f'\n{text}\n'

    return text


async def MessageSaverTELCON2(message: Message, update_id: str):
    print('🍎 update_id: ', update_id)
    print('🍎', yaml.dump(message, default_flow_style=False))

    store = pathlib.Path(CHATS_STORE)

    chat_id = chat_id_sanitize(message.chat.id.__str__())

    chat_unique_name = config.CHAT_DIRNAME_TEMPLATE.substitute(chat_id=chat_id)
    chat = store.joinpath(chat_unique_name)
    if not chat.exists():
        chat.mkdir(parents=True, exist_ok=True)

    chat_about = chat.joinpath('about.yml')
    if chat_about.exists():
        chat_about_text = read_file(chat_about)
        chat_about_data = yaml.load(chat_about_text, Loader=yaml.Loader)
        if title := chat_about_data.get('title'):
            if title != message.chat.title:
                chat_about_data = {
                    'title': message.chat.title,
                    'id': chat_id
                }
                chat_about_text = yaml.dump(
                    chat_about_data,
                    default_flow_style=False,
                    sort_keys=False,
                    allow_unicode=True,
                )
                write_file(chat_about, chat_about_text)
    else:
        chat_about_data = {
            'title': message.chat.title,
            'id': chat_id
        }
        chat_about_text = yaml.dump(
            chat_about_data,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )
        write_file(chat_about, chat_about_text)

    post_unique_name = config.POST_FILENAME_TEMPLATE.substitute(post_id=message.message_id)
    post = chat.joinpath(post_unique_name)

    context = dict()

    context['message'] = message
    context['data'] = {
        'text_markdown': '',
        'text_html': '',
        'photo': ''
    }

    if message.text:
        context['data']['text_markdown'] = message.text_markdown_v2_urled,
        context['data']['text_html'] = message.text_html

    if message.photo:
        photo_file = await message.photo[-1].get_file()
        ext = 'jpg'
        if photo_file.file_path:
            if exts := photo_file.file_path.split('.'):
                if ext_last := exts[-1]:
                    ext = ext_last

        photo_unique_name = config.PHOTO_POST_FILENAME_TEMPLATE.substitute(
            post_id = message.message_id,
            ext = ext
        )
        photo = chat.joinpath(photo_unique_name)

        await photo_file.download_to_drive(photo.as_posix())

        context['data']['photo'] = photo.name

        text_html = photo.name
        if hasattr(message, 'caption'):
            text_html = message.caption_html
        context['data']['text_html'] = text_html

    text = yaml.dump(
        context,
        default_flow_style=False,
        sort_keys=False,
        allow_unicode=True,
    )

    write_file(post, text)



