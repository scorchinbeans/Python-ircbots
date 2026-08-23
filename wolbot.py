#! /usr/bin/env python
# (C) Paulus Madison Hay
# License: gplv3

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
from bot_boilerplate import boilerplate
from os import system, environ
import socket, struct
mainclass = 'wolbot'

def wake_on_lan(macaddress): 
	# Check macaddress format and try to compensate.
    	if not (len(macaddress) == 12): # cslash
		if len(macaddress) == 17: # cslash
			sep = macaddress[2] # Fadly
			macaddress = macaddress.replace(sep, '') # fadly
        	else:
			raise ValueError('Incorrect \
			 MAC address format') # fadly
 
	# Fadly Tabrani {
    	# Pad the synchronization stream.
    	data = ''.join(['FFFFFFFFFFFF', macaddress * 20])
    	send_data = '' 

    	# Split up the hex values and pack.
    	for i in range(0, len(data), 2):
        	send_data = ''.join([send_data,
                              	     struct.pack('B', int(data[i: i + 2], 16))])

    	# Broadcast it to the LAN.
    	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    	sock.sendto(send_data, ('<broadcast>', 7))

class wolbot(boilerplate):
    def startbot(self, opts):
        nick, server, port = opts['nick'], opts['server'], opts['port']
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nick, nick)
        irc.client.ServerConnection.buffer_class.encoding = "latin-1"
        self.channel = channel
        self.server = server
        self.port = port

    def on_privmsg(self, c, e):
        cmd = e.arguments[0].split(' ')
        if cmd[0] == "!start":
            wake_on_lan(cmd[1])

    def do_command(self, e, cmd):
        nick = e.source.nick
        c = self.connection

        if cmd == "disconnect":
            self.disconnect()

        elif cmd == "die":
            self.die()

        elif cmd == "stats":
            for chname, chobj in self.channels.items():
                c.notice(nick, "--- Channel statistics ---")
                c.notice(nick, "Channel: " + chname)
                users = sorted(chobj.users())
                c.notice(nick, "Users: " + ", ".join(users))
                opers = sorted(chobj.opers())
                c.notice(nick, "Opers: " + ", ".join(opers))
                voiced = sorted(chobj.voiced())
                c.notice(nick, "Voiced: " + ", ".join(voiced))

        elif cmd == "dcc":
            dcc = self.dcc_listen()
            c.ctcp(
                "DCC",
                nick,
                f"CHAT chat {ip_quad_to_numstr(dcc.localaddress)} {dcc.localport}",
            )

        else:
            c.notice(nick, "Not understood: " + cmd)
