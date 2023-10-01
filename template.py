#!/usr/bin/env python


from utils import write_file

from jinja2 import Environment, BaseLoader, Template, FileSystemLoader

from flask_bootstrap import Bootstrap5

def make():
    template = Environment(loader=FileSystemLoader("templates")).get_template("base.html")

    context = dict()
    context['title'] = 'Title'
    context['content'] = 'CONTENT'

    write_file('render.html', template.render(context))


if __name__ == '__main__':
    print('🏀', 'Template')

    make()

