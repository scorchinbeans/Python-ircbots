#! /usr/bin/env python
# (C) Paulus Madison Hay

"""A simple example bot.

This is an example bot that uses the SingleServerIRCBot class from
irc.bot.  The bot enters a channel and listens for commands in
private messages and channel traffic.  Commands in channel messages
are given by prefixing the text by the bot name followed by a colon.
It also responds to DCC CHAT invitations and echos data sent in such
sessions.

The known commands are:

    stats -- Prints some channel information.

    disconnect -- Disconnect the bot.  The bot will try to reconnect
                  after 60 seconds.

    die -- Let the bot cease to exist.

    dcc -- Let the bot invite you to a DCC CHAT connection.
"""

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
