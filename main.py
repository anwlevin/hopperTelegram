#!/usr/bin/env python

import pprint

from telegram import ForceReply, Update
from telegram.ext import Application, ApplicationBuilder, MessageHandler, filters, ContextTypes
from urlextract import URLExtract
import pathlib

from utils import write_file


def getFirstYoutubeUrl(text):
    extractor = URLExtract()
    urls = extractor.find_urls(text)
    for url in urls:
        if 'youtube.com' in url:
            return url
        if 'youtu.be' in url:
            return url

    return None

def allDoings(text, date, id):

    url = getFirstYoutubeUrl(text)
    if not url:
        return

    print('🎥', url)

    name = f'posts/post-{date.strftime("%Y%m%d-%H%M%S")}-{id}.md'

    out = ''
    out += '\n'
    out += f'{url}'
    out += '\n'

    write_file(name, out)



async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('🍎', 'Update')
    #pprint.pprint(update)

    if update.channel_post:
        allDoings(update.channel_post.text, update.channel_post.date, update.channel_post.id)

    if update.message:
        allDoings(update.message.text, update.message.date, update.message.id)




TOKEN = '6324951837:AAHafdXmBOA4c5PfNPTSfib4lkEiUlFna_o'

if __name__ == '__main__':
    print('🏀', 'main.py')

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)
