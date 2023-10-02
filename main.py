#!/usr/bin/env python

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

import config
import message_saver


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('🍎', 'Update ')

    if update.channel_post:
        await message_saver.MessageSaverTELCON2(update.channel_post, update.update_id)

    if update.message:
        await message_saver.MessageSaverTELCON2(update.message, update.update_id)


TOKEN = '6324951837:AAHafdXmBOA4c5PfNPTSfib4lkEiUlFna_o'

if __name__ == '__main__':
    print('🏀', 'main.py')

    if not config.CHATS_STORE.exists():
        config.CHATS_STORE.mkdir(parents=True, exist_ok=True)

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)
