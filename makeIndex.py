
import pathlib

from main import getFirstYoutubeUrl
from utils import read_file, write_file

ROOT = 'posts'



def makeIndex():
    print('🏄️', 'Make Index')
    root = pathlib.Path(ROOT)
    files = list(root.iterdir())
    posts = list(filter(lambda file: file.name.startswith('post'), files))
    text = '\n'
    for post in posts:
        print(post)
        data = read_file(post)
        url = getFirstYoutubeUrl(data)

        text += f'### {post.relative_to(ROOT)}'
        text += '\n'
        text += '\n'
        text += f'{url}'
        text += '\n'
        text += '\n'
        text += '\n'
        text += '\n'
    text += '\n'

    name = 'posts/index.md'
    write_file(name, text)



