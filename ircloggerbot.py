#! /usr/bin/env python
# (C) Paulus Madison Hay
# License: gplv3

# Logs irc traffic on every channel
# it is commanded to join.

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
from bot_boilerplate import boilerplate
mainclass = 'ircloggerbot'
from os import system

class ircloggerbot(boilerplate):
    def startbot(self, opts):
        self.channel = opts['chan']
        self.server  = opts['serv']
        self.port    = opts['port']

    # List results.
    def on_list(self, c, e):
        c.join(e.arguments[0])

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.list()

    def on_pubmsg(self, c, e):
        rchan = e.target
        self.chanlog[e.target] \
         += e.arguments[0]
