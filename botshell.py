#! /usr/bin/env python

"""The neon saturn botnet.
(C) Paulus Madison Hay.
aka: dreadlink

license: gplv2
This is The neon saturn botnet controller.
It is used to start, maintain, and manipulate
irc bots started from its server."""

"""Bots written for this control system
must apply the irc.bot.SingleServerIRCBot
interface within their classes, to make
a central bot class inheriting the
bot_boilerplate.boilerplate class
which is then pointed to by the
mainclass variable."""

import time
from threading import Thread
import schedule, time, random
#from bitdollarbot import bitvoucherbot
from importlib import import_module
from os import popen, system
from os.path import dirname
from os.path import abspath
from os.path import exists
time.clock = time.time
from sys import stdout
from sys import exit
import json

homepath = __file__
homepath = abspath(homepath)
homepath = dirname(homepath)

autojoin = False
bots = []
nbot = 0

help = """help:
set [var] [val]
Set the environment variable
named [var] to value [val].
If no arguments, just show
all the environent varibles.

startbot [botname]
Will start a server thread with next
([nick] + botnr) nickname/botname.\n

listbots
Will list bots already started
by their nicknames.\n

analytics [start/stop]
Start or stop the analytics robot.

[botx] join [chan]
Join channel [chan]

[botx] status
Show server status dictionary.
Compatible bots must avail the
self.status dictionary. Here
it is displayed.\n

[botx] analytics autojoin
If the command [analytics autojoin] is
specified, will join *ajtopx most popular
channels on server every *ajtiming seconds.
If the command [analytics show] is given
instead, will only show those channels\n

[botx] kill
Kill bot [botx]

How to start and configure a bot:
>> set server irc.rizon.org
>> set port 6667
>> set nick georgie
>> startbot blkjackbot
blkjackbot0 started!
blkjackbot0 status
started: True
blkjackbot0 join #comedy
Server is started. Will
now start gambling."""

ajbot, rounds, config = None, 0, {}
auto_join, bot_servs = False, {}
bot_threads, botno = {}, 0

# initialize electrum.
system("electrum stop")
system('electrum daemon -d')

# Load config defaults.
config["nick"] = "thisbot"
config["channel"] = "#ownchan"
config['server'] = "irc.rizon.net"
config['port'] = 6697
config['ssl'] = True

print("Welcome to botshell.")
print("(C) Neon Saturn technate\n")

print("This application controls the irc")
print('bot services. Type "help" for usage')
print("instructions.")

while 1:
    cmd = input(">>")
    scmd =cmd.split(' ')
    if scmd[0] != "botshell" \
     and scmd[-1] != "end": pass
    if cmd == "exit":
        for t in bots:
            t.terminate()
            while not t.completed:
                pass # pause until
                     # terminated.

        print("Bots terminated.")
        print("Exiting cleanly.")
        exit()

    # These are the main commands
    if scmd[0] == "set":
        if len(scmd) == 1:
            for x in config.keys():
                print(x + ">> ", end='')
                print(config[x])
                print("")

        elif len(scmd) == 2: print(config[scmd[1]])
        elif len(scmd) == 3: config[scmd[1]] = scmd[2]
        else: print("[ERROR] Set command misused.")

    if scmd[0] == "startbot":
        botservname = scmd[1] # Name bot server
        if botservname not in bot_servs.keys():
            continue  # Check bot existence

        ss = config
        # Pass control over bots.
        ss['botifs'] = bot_threads
        botname = botservname + str(botno)
        if len(scmd) >= 3: ss['server'] = scmd[2]
        if len(scmd) == 4: ss[ 'port' ] = scmd[3]
        bs = eval('bot_servs[botservname].%s(ss)' \
         % bot_servs[botservname].mainclass)
        print("Started robot: " + botname)
        bt = Thread(target = bs.start)
        bt.start() # Start an thread.
        bot_threads[botname]  = [bs]
        bot_threads[botname] += [bt]
        botno += 1
        continue

    if scmd[0] == "listbots":
        print("Bot servers available")
        for i in bot_servs.keys(): print(i)
        print("\nActive bot threads:")
        for i in bot_threads.keys():
            print(i)

    if scmd[0] == "import":
        mod = import_module(scmd[1])
        bot_servs[scmd[1]] = mod

    if scmd[0] == "help":
        print(help)
        continue

    # These are the {[bot] [command] [oper]} conditions.
    if not scmd[0] in bot_threads.keys(): continue
    cmd = scmd[1:] # Shift cmd phrase.
    nbot = bot_threads[scmd[0]][0]
    nbot_name = scmd[0]

    if cmd[0] == "status":
        s = nbot.status # Status.
        s['chans'] = nbot.channels.keys()
        if len(cmd) == 3:
            if cmd[1] == "users":
                usrs = nbot \
                 .channels[cmd[2]] \
                 .users() # Users here
                s['chan_users'] = usrs

        for i in s.keys():
            print(i + " = ", end='')
            print(s[i])
            print('\n')

    elif cmd[0] == "kill":
        nbot.disconnect() # Exit
        nbot.die() # Kill bot thread.
        bot_threads[nbot_name][1].join()
        del(bot_threads[nbot_name])
        coninue

    else: nbot.do_command(' '.join(cmd))

# Advantages to profiteering through irc:
# The business may be run with sporadic
# access to the internet, wheras with
# HTTP, you need dedicated internet
# hosting.

# Using statbot, you can find all of
# the most popular channels in real
# time, on which to conduct the most
# business. Much more powerful than
# a website, which is only in one
# place.
