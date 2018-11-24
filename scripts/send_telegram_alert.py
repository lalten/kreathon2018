#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telegram_send

s1 = 'Hallo Nutzer! Morgen wird die blaue Tonne abgeholt!'
s2 = 'Schicke /kein_blau wenn die Tonne noch nicht halb voll ist um die Umwelt zu schonen!'

telegram_send.send(messages=[s1, s2])