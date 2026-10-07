#! /usr/bin/env python
#
# 925268 - WALBOT(TM)
# IRC REST interface bitcoin
# wallet. Recieves an electrum
# shell command and outputs
# electrum's json output.
# (C) Paulus Madison Hay

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
from bot_boilerplate import boilerplate
from os import system, environ
import socket, struct
mainclass = 'walbot'

class walbot(boilerplate):
    def startbot(self, opts):
        nick, server, port = opts['nick'], opts['server'], opts['port']
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nick, nick)
        irc.client.ServerConnection.buffer_class.encoding = "latin-1"
        self.channel = channel
        self.server = server
        self.port = port

    def on_privmsg(self, c, e):
        cmd = e.arguments[0].split(' ')
        if cmd[0] == "!electrum":
            cmd = ' '.join(cmd[1:])
            x = popen('electrum %s' % cmd, 'r')
            e.privmsg(e.source.nick, x.read ())

        if cmd[0] == "!adduser":
            tc = f'electrum {walad}/{cmd[1]}' \
             f' create --password "{cmd[2]}"'
            x = popen(tc + cmd[1], 'r').read()
            e.privmsg(e.source.nick, x)
