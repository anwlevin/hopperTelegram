#!/usr/bin/env python

import pathlib

import telegram
import yaml
from jinja2 import Environment, FileSystemLoader
from urlextract import URLExtract

from config import STORE
from message_saver import message_text_filter
from utils import read_file, write_file
from markdownify import markdownify as md

def text_Preprocessing(text_html):
    print('🦜', 'Preprocessing text: ')
    print(text_html)
    print('==============')


    for url in URLExtract().find_urls(text_html):
        text_html = text_html.replace(url, f'<a href="{url}">{url}</a>')

    #text_html = md(text_html)
    text_html = text_html.replace('\n', '<br>\n')

    #print('🦜🦜')
    #print(text_html)
    #print('==============')

    #print()
    #print()

    return text_html


def renderPostCard(message: telegram.Message, data: dict):
    template = Environment(loader=FileSystemLoader("templates")).get_template("post.html")
    return template.render(
        {'title': f'Post {message.message_id}',
         'date': message.date.__str__(),
         'content': text_Preprocessing(data.get('text_html')),
         })


def indexChat(chat):
    files = chat.iterdir()
    posts = sorted(list(filter(lambda file: not file.name.startswith('index'), files)), reverse=True)

    content = ''
    content += '<div class="col-md-8 mx-auto">'
    for post in posts:
        text_post = read_file(post)
        yaml_post = yaml.load(text_post, Loader=yaml.Loader)

        message_post = yaml_post.get('message')
        data_post = yaml_post.get('data')

        content += renderPostCard(message_post, data_post)
    content += '</div>'

    title = chat.__str__()
    template = Environment(loader=FileSystemLoader("templates")).get_template("base.html")
    write_file(chat.joinpath('index.html'), template.render({'title': title, 'content': content}))


def indexAllChats():
    print('💎️', 'Make Index')
    store = pathlib.Path(STORE)

    files = store.iterdir()
    files = sorted(list(filter(lambda file: not file.name.startswith('index'), files)), reverse=True)
    for chat in files:
        indexChat(chat)


if __name__ == '__main__':
    indexAllChats()
