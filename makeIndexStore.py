#!/usr/bin/env python

import pathlib

from jinja2 import Environment, FileSystemLoader, Template

from config import STORE
from utils import write_file


def indexDir(current_dir):
    print('💎️', 'Make index Dir')

    files = current_dir.iterdir()
    files = list(filter(lambda file: not file.name.startswith('index'), files))

    title = f'Index of {current_dir}'

    content = ''
    content += '<ul>'
    for file in files:
        a_content = Template('<h3><a href="{{ href }}">{{ content }}</a></h3>').render({
            'href': file.relative_to(current_dir).as_posix(),
            'content': file.relative_to(current_dir)
        })
        content += Template('<li>{{ content }}</li>')\
            .render({'content': a_content})
    content += '</ul>'

    template = Environment(loader=FileSystemLoader("templates")).get_template("base.html")
    write_file(current_dir.joinpath('index.html'), template.render({'title': title, 'content': content}))


if __name__ == '__main__':
    store = pathlib.Path(STORE)
    indexDir(store)
