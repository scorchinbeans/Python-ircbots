#! /usr/bin/env python

# An irc advertisement robot.
# By: Paulus Madison Hay

import irc.bot
import irc.strings
from bot_boilerplate import boilerplate
from irc.client import ip_numstr_to_quad
from irc.client import ip_quad_to_numstr
from os.path import exists
mainclass = 'adnetbot'
from os import system
from time import time
import schedule
import json

class adnetbot(boilerplate):
    def bot_init(self, opers):
        self.cfgfn = "config.dat"
        self.server = opers['server']
        self.port = opers['port']
        self.irc_shows = []
        self.t_lastad  = {}

        self.traffic = 0
        self.status  = {}
        self.ses_ads = []
        self.irc_ads = {}
        self.chans   = []
        self.irc_adnow = 0
        self.irc_adnick = 'self'
        self.irc_ads['ads'] = {}
        if not exists(self.cfgfn):
            self.irc_ads['self'] = \
             ["""[your ad here!] pm this
             bot !help for help."""] # Shows
            self.irc_ads['ads']['self'] = -1
            system("touch " + self.cfgfn)
            self.updateconfig()

        else:
            x = open(self.cfgfn, 'r')
            cfg = json.loads(x.read())
            self.irc_ads = cfg['irc_ads']
            x.close()

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def bot_welcome(self, c, e):
        schedule.every(5).seconds.do(self.timead)
        self.ready = True

    def on_privmsg(self, c, e):
        arg = e.arguments[0].split(' ')
        nick = e.source.nick

        if nick == "self": return
        if nick in self.multi.keys():
            if self.multi[nick] == "ircad-multiline":
                msg = ' '.join(arg)
                if msg == "end": # Post tmp irc ad.
                    txt_ad = '\n'.join(self.tmp_irc_ad)
                    self.irc_ads[nick] += [txt_ad]
                    self.irc_ads['ads'][nick] += 1
                    del(self.multi[nick])
                    updateconfig()

                # Fill tmp irc ad.
                else: self. \
                 tmp_irc_ad \
                 += msg +"\n"

        if arg[0] == "!buy-irc-ad":
            show = arg[1] # of ads.
            cost =show * self.price
            self.irc_ads[nick] = []
            if not self.checkout(nick, cost):
                if len(arg) > 2:
                    msg = ' '.join(arg[2:])
                    self.irc_ads[ nick] += [msg]
                    self.irc_ads['ads'][nick] = show
                    updateconfig()
                    return

                self.multi[nick] = \
                 'ircad-multiline'
                c.privmsg(nick, \
                 "Checked out %d ads for \
                 %f btc" % (nick, cost))
                return

        elif arg[0] == "!help":
            c.privmsg(nick, "!buy-irc-ad [#shows] [message]")
            c.privmsg(nick, "Buy an advertisement, [message]")
            c.privmsg(nick, "to be shown [#shows] times.")

    def on_pubmsg(self, c, e):
        if e.target not in self.chans: return
        self.traffic = (self.traffic + 1) % 40
        if self.traffic != 0: return
        self.t_lastad[e.target] = time()
        self.iter_ads()

        iads = self.irc_ads
        iads['self'] += self.ses_ads
        for l in iads[self.irc_adnick] \
         [self.irc_adnow].split('\n'):
            c.privmsg(e.target, l)

    def on_join(self, c, e):
        self.chans += [e.target]
        s = self.irc_ads['self'][0]
        self.t_lastad[e.target] = time()
        for l in s.split('\n'): \
            c.privmsg(e.target, l)

        self.iter_ads()

    def on_kick(self, c, e):
        c.join(e.target)

    def updateconfig(self):
        cfg = {} # cfg contains config data
        cfg['irc_ads'] = self.irc_ads
        x = open(self.cfgfn, 'w')
        x.write( json.dumps(cfg))
        x.close()

    def checkout(self, nick, cost):
        c = self.connection # Charge [nick], [cost].
        c.privmsg(nick, "cost: %f bitcoins" % cost)
        cc = "electrum add_request %f" % cost

        ep = popen(cc, "r")
        reqjson = json.loads(ep.read())
        rid = reqjson["request_id"]
        htm = reqjson["URI"]

        cc = "electrum get_request %s" % rid
        c.privmsg(nick, "Send bitcoins through")
        c.privmsg(nick, "this link. You have 30")
        c.privmsg(nick, "seconds before timeout")
        c.privmsg(nick, htm)

        bc = time.time() + 30
        while time.time() <= (bc + 30):
            ep = popen(cc, "r")
            rstr = json.loads(ep.read())
            rstr = rstr["status_str"]
            ep.close()
            sleep(3)

        if rstr == "Completed": return 0
        else: return 1

    def cmd_parser(self, command):
        cmd = command.split(' ')
        if cmd[0] == "join":
            self.connection.join(cmd[1])

        elif cmd[0] == "store-ad":
            msg = ' '.join(cmd[1:])
            self.irc_ads[ 'self' ] += [ msg]
            self.updateconfig()

        elif cmd[0] == "ses-ad":
            self.ses_ads += \
             [' '.join(cmd[1:])]

        elif cmd[0] == "list-ads":
            print("Session ads:")
            print("\n".join(self.ses_ads))
            print("\n\nStored ads:")
            print(json.dumps(self.irc_ads))

        elif cmd[0] == "help":
            print("""Help:
            join [channel]: Join a channel")
            store-ad [ad]: Add your [ad] to self ads
            in config file.

            ses-ad [ad]: Add your [ad] to session
            ads in local variable.

            list-ads: List the ads
            to be shown.""")

    def timead(self):
        for k in self.t_lastad.keys():
            if time() - self. \
             t_lastad[k] >= 30:
                self.iter_ads()
                self.t_lastad[k] = time()
                for l in iads[self.irc_adnick] \
                 [self.irc_adnow].split('\n'):
                    self.connection.privmsg(k, l)

    def iter_ads(self):
        self.irc_adnow = (self.irc_adnow + 1) \
         % len(self.irc_ads[self.irc_adnick])
        if self.irc_adnow == 0:
            self.irc_ads['ads'] \
             [self.irc_adnick] -= 1

            nicks = list(self.irc_ads.keys())
            nick_ind = nicks.index(self.irc_adnick)
            nick_ind = (nick_ind + 1) % len( nicks)
            if nicks[nick_ind] == "ads": nick_ind \
             = (nick_ind + 1) % len(nicks) # skip.
            self.irc_adnick = nicks[nick_ind]
            self.updateconfig()
