#!/usr/bin/env python
import pathlib
from string import Template

CHATS_STORE = pathlib.Path('store')

CHAT_DIRNAME_TEMPLATE = Template('chat-${chat_id}')

POST_FILENAME_TEMPLATE = Template('post-${post_id}.yml')

PHOTO_POST_FILENAME_TEMPLATE = Template('post-${post_id}-photo.${ext}')



