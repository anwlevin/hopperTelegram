#!/usr/bin/env python
import json
import pathlib
import pprint
from string import Template

import telegram
import yaml
from jinja2 import Environment, FileSystemLoader
from urlextract import URLExtract

from config import STORE
from message_saver import message_text_filter
from utils import read_file, write_file
from markdownify import markdownify as md

def text_Preprocessing(text_html):
    text_html = str(text_html)
    print('🦜', 'Preprocessing text: ')
    print(text_html)
    print('==============')

    if urls := URLExtract().find_urls(text_html):
        for url in urls:
            text_html = text_html.replace(url, f'<a href="{url}">{url}</a>')

    text_html = text_html.replace('\n', '<br>\n')

    return text_html


def renderForwardPostContent(message: telegram.Message, data: dict):
    print('🛍 Forward')
    print('Message: ')
    print(message)
    print('===========')
    print()
    print()

    contents = []

    forw_chat = ''
    if hasattr(message, 'forward_from_chat'):
        if hasattr(message.forward_from_chat, 'title'):
            forw_chat += f'<strong>{message.forward_from_chat.title}</strong>'

        if hasattr(message.forward_from_chat, 'username'):
            forw_chat += f'<small>({message.forward_from_chat.username})</small>'

        if hasattr(message.forward_from_chat, 'id'):
            forw_chat += f' <small>[{message.forward_from_chat.id}]</small>'

    contents.append(f'<h5>{forw_chat}</h5>')

    if hasattr(message, 'forward_date'):
        contents.append(f'<p>{message.forward_date}</p>')

    contents.append(f'TEXT')
    contents.append('==========')
    contents.append(text_Preprocessing(data.get('text_html')))

    content = '<br>'.join(contents)

    forw_templ = '''
    <div class="border border-primary ml-2 pl-3" 
        style="
            border-right: none!important;
            margin-left: .5rem;
            padding-left: 1rem;
            border-bottom: none!important;
            border-top: none!important;
            border-width: 1px!important;">
            $content
            </div>
            '''

    content = Template(forw_templ).substitute(content=content)

    return content

    template = Environment(loader=FileSystemLoader("templates")).get_template("forwardPostContent.html")
    return template.render(
        {'title': f'Post {message.message_id}',
         'date': message.date.__str__(),
         'content': content,
         })

def renderPostCard(message: telegram.Message, data: dict):
    #print('🖼 ', message.message_id)
    #print(yaml.dump(message, default_flow_style=False))
    #print('========')
    #print()
    #print()
    #print()

    content = ''
    if hasattr(message, 'forward_date') and message.forward_date:
        content = renderForwardPostContent(message, data)
    else:
        content = text_Preprocessing(str(data.get('text_html')))

    template = Environment(loader=FileSystemLoader("templates")).get_template("post.html")
    return template.render(
        {'title': f'Post {message.message_id}',
         'date': message.date.__str__(),
         'content': content,
         'photo': data.get('photo')
         })


def indexChat(chat):
    print(chat)
    files = chat.iterdir()
    posts = sorted(list(filter(lambda file: not file.name.startswith('index') and file.name.endswith('.yml'), files)), reverse=True)

    content = ''
    content += '<div class="col-md-8 mx-auto">'
    for post in posts:
        print(post)
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
