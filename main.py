#!/usr/bin/env python

import pprint

from telegram import ForceReply, Update
from telegram.ext import Application, ApplicationBuilder, MessageHandler, filters, ContextTypes
from urlextract import URLExtract
import pathlib

import message_saver
from config import CHATS_STORE
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


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('🍎', 'Update ')

    if update.channel_post:
        await message_saver.MessageSaverTELCON2(update.channel_post, update.update_id)

    if update.message:
        await message_saver.MessageSaverTELCON2(update.message, update.update_id)


def init_store_dir(store_dir_name=CHATS_STORE):
    store = pathlib.Path(store_dir_name)
    store.mkdir(parents=True, exist_ok=True)
    return store


TOKEN = '6324951837:AAHafdXmBOA4c5PfNPTSfib4lkEiUlFna_o'

if __name__ == '__main__':
    print('🏀', 'main.py')

    init_store_dir()

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)
