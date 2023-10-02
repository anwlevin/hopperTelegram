#!/usr/bin/env python

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

import config
import message_saver
import re

samples = '''
Philosophical. Notes - Uuuuuuuuuu-u
Philosophical. Archivium - Uuuuuuuuuu-u
Youtube Notes
Youtube Watch - Uuuuuuuuuu-u
Youtube Watch-Uuuuuuuuuu-u
Youtube Watch Uuuuuuuuuu-u
'''



CHAT_SMALL_TITLE_PATTENS = '''
.*( - Uuuu.*)
.*(- Uuuu.*)
.*(-Uuuu.*)
.*(Uuuu.*)
.*( - U-uuu.*)
.*(- U-uuu.*)
.*(-U-uuu.*)
.*(U-uuu.*)
'''

def cleanTitleWithPattern(text, pattern):
    if match := re.match(pattern, text):
        to_replace = match.group(1)
        return text.replace(to_replace, '')

    return text

def cleanTitleAllPatterns(text, patterns):
    for pattern in patterns:
        text = cleanTitleWithPattern(text, pattern)
    return text


if __name__ == '__main__':
    print('🏀 REGEXP')

    for sample in samples.strip().split('\n'):
        print('🎯 ', sample)
        sample = cleanTitleAllPatterns(sample, CHAT_SMALL_TITLE_PATTENS.strip().split('\n'))
        print('🎨', sample)

        print()
        print()


    print('🏀🏀 End')

