#! /usr/bin/python

import os
import logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

import requests

# class TransportationMode:
#     FOOT = 1
#     CAR = 2
#
#     def __init__(self):
#         pass

# class Conversation:
#     def __init__(self, user_id, mode=TransportationMode.FOOT):
#         self.user_id = user_id
#         self.mode = mode
#
#     def __str__(self):
#         return str(self.user_id) + ': ' + FirstChatBot._transport_mode_to_string(self.mode)


class FirstChatBot:
    TOKEN = '767777347:AAHWBUNY_eCCSftpRSNI4Tr7x-eorSv0UQo'
    rest_url = 'http://10.13.144.90:5000/containers'

    def __init__(self):

        self.with_webhooks = False

        self.conversations = dict()  # maps id to Conversation

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

        self.updater = Updater(token=self.TOKEN)

        if self.with_webhooks:
            self.updater.start_webhook(listen='127.0.0.1', port=8443, url_path=self.TOKEN)
            self.updater.bot.set_webhook(webhook_url='https://my_server.com/' + self.TOKEN,
                                         certificate=open('webhook_cert.pem', 'rb'))

        self.dispatcher = self.updater.dispatcher

        self.dispatcher.add_handler(CommandHandler("start", self.start))
        # self.dispatcher.add_handler(CommandHandler("mode", self.ask_for_mode))
        self.dispatcher.add_handler(CommandHandler("help", self.show_help))

        self.dispatcher.add_handler(MessageHandler(Filters.text, self.text_cb))
        self.dispatcher.add_handler(MessageHandler(Filters.location, self.got_location))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.mode_button_cb))

        self.get_containers()

    def get_containers(self):
        response = requests.get(self.rest_url, [])
        print response.json()['containers'][0]

    def show_help(self, bot, update):
        update.message.reply_text('Welcome! \n'
                                  'use these commands: \n'
                                  '- /mode to select transportation mode \n'
                                  '- send location to request route')

    # @staticmethod
    # def _transport_mode_to_string(mode):
    #     mode = int(mode)
    #     if mode == TransportationMode.FOOT:
    #         return "By Foot"
    #     if mode == TransportationMode.CAR:
    #         return "By Car"
    #     return "Unknown transportation mode " + str(mode)

    def ask_for_cleanliness(self, bot, update):
        # https://apps.timwhitlock.info/emoji/tables/unicode
        keyboard = [[InlineKeyboardButton("Bad \xF0\x9F\x91\x8E", callback_data='cl,1'),
                     InlineKeyboardButton("OK \xF0\x9F\x91\x8D", callback_data='cl,2'),
                     InlineKeyboardButton("Great \xF0\x9F\x91\x8F", callback_data='cl,3')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('How clean is the bootle bank?', reply_markup=reply_markup)

    # def ask_for_mode(self, bot, update):
    #     keyboard = [[InlineKeyboardButton("By Foot", callback_data="mode, %i" % TransportationMode.FOOT),
    #                  InlineKeyboardButton("By Car", callback_data="mode, %i" % TransportationMode.CAR)]]
    #
    #     reply_markup = InlineKeyboardMarkup(keyboard)
    #     update.message.reply_text('How do you want to travel:', reply_markup=reply_markup)

    def start(self, _, update):
        """Send a message when the command /start is issued."""

        user_id = update.message.chat.id
        fname = update.message.chat.first_name

        # user, created = User.objects.get_or_create(pk=user_id)
        # user.first_name = fname
        # user.message_count += 1
        # user.save()

        # if user_id in self.conversations:
        #     update.message.reply_text("Hello Back " + fname)
        # else:
        #     self.conversations[user_id] = Conversation(user_id)
        #     update.message.reply_text('Welcome ' + fname + '!')

    def _process_cleanliness_answer(self, user_id, value):
        return_text = "Cleanliness: {}".format(str(value)) + ' / 3'
        return return_text

    # def _process_mode_answer(self, user_id, value):
    #     return_text = "Selected Transportation mode: {}".format(self._transport_mode_to_string(value))
    #
    #     if user_id in self.conversations:
    #         self.conversations[user_id].mode = value
    #     else:
    #         self.conversations[user_id] = Conversation(user_id, mode=value)
    #
    #     return return_text

    def mode_button_cb(self, bot, update):
        assert isinstance(update, Update)
        assert isinstance(update.callback_query, CallbackQuery)
        user_id = update.callback_query.from_user.id

        query = update.callback_query

        ans = query.data.split(',')
        cmd = str(ans[0])
        value = int(ans[1])

        if cmd == 'cl':
            text = self._process_cleanliness_answer(user_id, value)
        if cmd == 'mode':
            text = self._process_cleanliness_answer(user_id, value)

        bot.edit_message_text(text=text, chat_id=query.message.chat_id, message_id=query.message.message_id)

    def text_cb(self, bot, update):
        # bot.send_message(chat_id=update.message.chat_id, text="Hello! use /start")
        self.ask_for_cleanliness(bot, update)
        # self.ask_for_mode(bot, update)

    def run(self):
        if not self.with_webhooks:
            self.updater.start_polling()
        self.updater.idle()

    def got_location(self, bot, update):
        assert isinstance(update, Update)
        bot.send_message(chat_id=update.message.chat_id, text="Thanks for sharing your location")
        print ("got location")
        # self.ask_for_mode(bot, update)
        # chat_id = update.message.chat.id
        # ght = GetHereTile()
        # fname = '/tmp/foo.jpg'
        # ght.get_image(update.message.location.latitude, update.message.location.longitude, fname)
        # bot.send_photo(chat_id=chat_id, photo=open(fname, 'rb'))


if __name__ == "__main__":
    fcb = FirstChatBot()
    fcb.run()
