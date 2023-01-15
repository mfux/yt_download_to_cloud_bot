#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import random
import re

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class RawTextReplier():
    def __init__(self, token, reply_function=None, start_message="Hi!"):
        self.token = token
        self.start_message = start_message
        # if no reply function was given, use the echo function
        if not reply_function:
            self.reply_function = self.echo
        else:
            self.reply_function = reply_function

    # Define a few command handlers. These usually take the two arguments update and
    # context. Error handlers also receive the raised TelegramError object in error.
    def start(self, update, context):
        """Send a message when the command /start is issued."""
        update.message.reply_text(self.start_message)

    @staticmethod
    def help(update, context):
        """Send a message when the command /help is issued."""
        update.message.reply_text('Help!')

    @staticmethod
    def echo(message):
        """Echo the user message."""
        return message

    @staticmethod
    def error(update, context):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)

    def reply(self, update, context):
        yt_pattern = r"http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?"
        if not re.findall(yt_pattern, update.message.text):
            return
        # construct informational message
        ok = random.choice(["ok", "na gut", "passt", "okay", "alles klar", "ja ok", "gut", "aye"])
        mach_ich = random.choice(["ich machs gleich", "wird erledigt", "wird gemacht", "mach ich gleich", "mach ich"])
        update.message.reply_text(f"{ok} {mach_ich}")
        answer = self.reply_function(update.message.text)
        update.message.reply_text(f"soo, hier ist der link zum herunterladen")
        update.message.reply_text(answer)

    def run(self):
        """Start the bot."""
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        updater = Updater(self.token, use_context=True)

        # Get the dispatcher to register handlerspip
        dp = updater.dispatcher

        # on different commands - answer in Telegram
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler("help", help))

        # on noncommand i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler(Filters.text, self.reply))

        # log all errors
        dp.add_error_handler(self.error)

        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()


if __name__ == '__main__':
    r = RawTextReplier()
    r.run()
