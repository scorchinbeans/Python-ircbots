#! /usr/bin/env python
# (C) Paulus Madison Hay
# License: gplv2

# Nickname service which registers someone's
# nickname or kicks them off the server.

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
from bot_boilerplate boilerplate
from os import system
mainclass = 'idbot'

class idbot(boilerplate):
    def __init__(self, opts):
        nick, server, port = opts['nick'], opts['server'], opts['port']
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nick, nick)
        irc.client.ServerConnection.buffer_class.encoding = "latin-1"
        self.newchan = opts['channel']
        self.server = server
        self.port = port
        self.layer = 3

        self.wait_input = {}
        self.input_recv = {}
        self.banned = []
        self .tries = {}

        # Create a new irc channel
        # on startup, so that the
        # operator is automatically
        # this bot.

        # Layer 1:
        # Password and nick/username
        # based authentication. Fuses
        # a nickname to a logged in
        # username and if the password
        # is wrong, it kicks you as
        # the operator.

        # Layer 2: Web authentication.
        # Using web based facial camera picture
        # taking script, send this script to
        # the user, taking his facial picture
        # then processing it with facial
        # recognition, as well as using
        # the layer 1 security technique.
        # If the user cannot provide a
        # facial picture, he will be
        # kicked.

    def chan_chk(self):
        users = self \
         .channels.items()[0].users()
        for u in users:
            # autokick if !logged_in
            if u not in self.logged_in:
                self.kick(u)

            # autokick if banned.
            if u not in self.banned:
                self.kick(u)

            if u not in self.users:
                elif not self.loginuser(u):
                    self.tries[u] += 1
                    if self.tries == 3:
                        self.banned += [u]
                        return

                else: self.logged_in += [u]
                self.users += u

        for u in self.users:
            if u not in users:
                del(self.users \
                 [self.users.index(u)])

    def get_input(self, user):
        self.wait_input[user] = True
        while not self \
         .input_recv[user]:
            pass

        x = self.input_recv[user]
        self.input_recv[user] = ""
        return

    def loginuser(self, nick):
        c.privmsg(nick, "Login or send an empty")
        c.privmsg(nick, "password to cancel the")
        c.privmsg(nick, "login and pm !adduser")
        c.privmsg(nick, "to create an account.")

        c.privmsg(nick, "Enter password: ")
        password = self.get_input(nick)
        if password == "": return False
        c.privmsg(nick, "Enter username: ")
        username = self.get_input(nick)
        pj = open('id_users.json', 'r').read()
        passwd = json.loads(pj) [username]
        if passwd['password'] == password:
            return True

        else: return False

    def bot_welcome(self, c, e)
        c.join(self.channel)
        schedule.every(5). \
         seconds.do(self.chan_chk)

    def on_privmsg(self, c, e):
        if self.wait_input[e.source.nick]:
            self.input_recv[user] = e.arguments[0]
            self.wait_input[e.source.nick] = False
            return

        nick = e.source.nick
        if arguments[0] == '!logout':
            i = self.logged_in.index(nick)
            del(self.logged_in[i])

        elif arguments[0] == "!adduser":
            c.privmsg("username: ")
            username = self.get_input(nick)
            c.privmg("password: ")
            password = self.get_input(nick)
            j = open('id_users.json', 'r').read()
            jj = open('id_users.json', 'w')
            j = json.loads(j.read())
            j[username]['password'] \
             = password
            jj.write(json.dumps(j))
            jj.close()

