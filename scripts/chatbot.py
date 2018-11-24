#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import logging
import re
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

import requests

from here_connector import calc_route, route_to_image


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

        self.dispatcher.add_handler(CommandHandler("start", self.on_start))
        self.dispatcher.add_handler(CommandHandler("help", self.on_help))

        conv_handler_nearest = ConversationHandler(
            entry_points=[CommandHandler("near", self.conv_nearest_start)],
            states={
                'LOCATION_NEAR': [MessageHandler(Filters.location, self.conv_nearest_loc)]
            },
            fallbacks=[]
        )
        self.dispatcher.add_handler(conv_handler_nearest)

        self.rate_container_id = 0
        conv_handler_rate = ConversationHandler(
            entry_points=[CommandHandler("rate", self.conv_rate_start)],
            states={
                'LOCATION_RATE': [MessageHandler(Filters.location, self.conv_rate_loc)],
                'CONFIRM': [MessageHandler(Filters.text, self.conv_rate_confirm)],
                'RATE': [MessageHandler(Filters.text, self.conv_rate_done)]
            },
            fallbacks=[MessageHandler(Filters.all, self.conv_rate_stop)]
        )
        self.dispatcher.add_handler(conv_handler_rate)

    def conv_rate_start(self, bot, update):
        update.message.reply_text('Which container do you want to provide feedback for? '
                                  'Please send the location of the container you want to rate.')
        return 'LOCATION_RATE'

    def conv_rate_stop(self, bot, update):
        update.message.reply_text(u'Sorry, I don\'t understand 😟. If you want to try again, use the /rate command ☝️.')
        return ConversationHandler.END

    def conv_rate_loc(self, bot, update):
        user_location = update.message.location
        url = 'http://10.13.144.90:5000/get_closest'
        data_dict = {"lat": user_location.latitude, 'lng': user_location.longitude}
        response = requests.post(url, data_dict)
        container = response.json()['closest_container']
        self.rate_container_id = container['closest_container_id']
        descr = container['location_string'].rstrip()
        reply_keyboard = [[KeyboardButton(u"Yes 👌"), KeyboardButton(u"No 🚫")]]
        update.message.reply_text(u'The container closest to that location is #{} at {}. Is that the one you want to rate?'.format(self.rate_container_id, descr),
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return 'CONFIRM'

    def conv_rate_confirm(self, bot, update):
        if 'No' in update.message.text:
            update.message.reply_text('Sorry, please try again by sending the /rate command.')
            return ConversationHandler.END
        reply_keyboard = [[KeyboardButton(u"More of this 😍"), KeyboardButton(u"Please fix 😨")]]
        update.message.reply_text('OK! How do you rate the container?',
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return 'RATE'

    def conv_rate_done(self, bot, update):
        feedback = 0
        if 'More' in update.message.text:
            feedback = +1
        elif 'fix' in update.message.text:
            feedback = -1
        else:
            return self.conv_rate_stop(bot, update)
        ok = self.send_feedback(clean=feedback, user=update.message.from_user)
        if ok:
            update.message.reply_text('Thank you for your feedback!')
        else:
            update.message.reply_text('Oops, that didn\'t work out! Please try again later.')
        return ConversationHandler.END

    def conv_nearest_start(self, bot, update):
        location_keyboard = [[KeyboardButton(text="send location", request_location=True)]]
        update.message.reply_text('We\'ll get you to the next container ASAP! Please share your location.',
                                  reply_markup=ReplyKeyboardMarkup(location_keyboard, one_time_keyboard=True))
        return 'LOCATION_NEAR'

    def conv_nearest_loc(self, bot, update):
        user_location = update.message.location
        url = 'http://10.13.144.90:5000/get_best'
        data_dict = {"lat": user_location.latitude, 'lng': user_location.longitude}
        response = requests.post(url, data_dict)
        container = response.json()['best_container']
        pos = container['closest_container_pos']
        id = container['closest_container_id']
        descr = container['location_string'].rstrip()
        s = ["%f,%f" % (data_dict['lat'], data_dict['lng']), pos]
        route = calc_route(s, 'pedestrian')
        img_url = route_to_image(route)
        bot.sendPhoto(update.message.chat_id, img_url,
                      caption=u'Container {} at {} is the best place for you to drop your litter! 🚮'.format(id, descr))
        return ConversationHandler.END

    def send_feedback(self, clean, user):
        url = 'http://10.13.144.90:5000/feedback'
        data_dict = {"user_id": user.id, "first_name": user.first_name, "container_id": self.rate_container_id, "clean": clean}
        response = requests.post(url, data_dict)
        return response.ok

    def on_help(self, bot, update):
        update.message.reply_text(u'If you send /near I will provide the best available garbage container for you. \n'
                                  u'If you send /rate, You can leave feedback for a container ☺️')

    def ask_for_cleanliness(self, bot, update):
        # https://apps.timwhitlock.info/emoji/tables/unicode
        keyboard = [[InlineKeyboardButton("Bad \xF0\x9F\x91\x8E", callback_data='cl,1'),
                     InlineKeyboardButton("OK \xF0\x9F\x91\x8D", callback_data='cl,2'),
                     InlineKeyboardButton("Great \xF0\x9F\x91\x8F", callback_data='cl,3')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('How clean is the bootle bank?', reply_markup=reply_markup)

    def on_start(self, bot, update):
        """Send a message when the command /start is issued."""
        user_id = update.message.chat.id
        fname = update.message.chat.first_name
        update.message.reply_text(u'Hi {}! Can\'t wait to do my thing here 😎\n Send your location or type /help'.format(fname))

    def run(self):
        if not self.with_webhooks:
            self.updater.start_polling()
        self.updater.idle()


if __name__ == "__main__":
    fcb = FirstChatBot()
    fcb.run()
