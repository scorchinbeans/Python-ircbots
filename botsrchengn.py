#! /usr/bin/env python
# (C) Paulus Madison Hay
# License: gplv3

# Is a search engine for bots. Scans
# each channel's header and searches
# through that text to help a user
# find an irc channel, and can be
# PM'd with the location or nickname
# of a bot on the irc server, to
# also be indexed and accessible
# through the search engine.

import irc.bot
import irc.strings
from time import strftime
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
mainclass = 'botsrchengn'
from os import system
sat = 0.00000001
import rsa

class botsrchengn(boilerplate):
    def startbot(self, opts):
        nick, server, port = opts['nick'], opts['server'], opts['port']
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nick, nick)
        irc.client.ServerConnection.buffer_class.encoding = "latin-1"
        self.channel = channel
        self.xdate = "0/2/0"
        self.rescost = 20
        self.server = server
        self.port = port
        self.tout = 2

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_list(self, c, e):
        self.chans += [e.target]

    def on_listend(self, c, e):
        self.listend = True

    def on_liststart(self, c, e):
        self.listend = False

    def bot_welcome(self, c, e):
        c.list() # Scan channels for indexible
        while not self.listend: pass # irc bots.
        for cc in range(0, len(self.chans), 4):
            for ch in range(cc, cc + 4): c.join(self.chans[ch])
            for chname, chobj in self.channels.items():
                u, v = chobj.users(), "searchbot v2.0"
                for us in u: self.send_ctcp(u, "VERSION", v)

            for ch in range(cc, cc + 4):
                c.part(self.chans[ch])

    def on_ctcp(self, c, e):
        if e.arguments[0] == "VERSION":
            i = e.arguments[1].lower().split('//')
            if (len(i) > 1) and (i[0] == 'svcbot'):
                self.metalog(' '.join(i[1:]))

    def on_privmsg(self, c, e):
        if ':' not in e.arguments[0]:
            return

        nick = e.source.nick
        x = e.arguments \
         [0].split(':')

        if x[0] == 'help':
            c.privmsg(e.target, "meta:[meta descr.] \
             Store meta information from your bot")
            c.privmsg(e.target, "search:[search query] \
             Search for terms.")

        if x[0] == 'meta':
            c.privmsg(e.target, "To add your service's \
             description to the meta database for searching \
             you must pay %d satoshis here. Your entry will \
             be removed after %d months of accessibility." \
             % (self.cost, self.tout))

            if x[1][0] == "!": # API key symbol found...
                if x[1] not in [i[0] for i in self.userinfo]:
                    c.privmsg(e.target, "API key not found!")
                    return

                else: # Using API key.
                    tmp = self.userinfo.index(x[1])
                    if self.userinfo[tmp] <= 0:
                        c.privmsg(e.target, "Out of slots!")
                        break

                    s = [i[0] for i in self \
                     .userinfo].index(x[0]) \
                    s = self.userinfo[s[3]]
                    ss = self.itrs[i[0]][0]
                    sa = self.itrs[i[0]][1]

                    # Create iterator.
                    slots = self.getvals(s)['slots']
                    if x[0] not in self.itrs.keys():
                        self.itrs[i[0]] = [0, slots]

                    # Iterate slots..
                    else: self.itrs[x[0]][0] = (ss + 1) % sa
                    s = [self.userinfo[i][1] if len(self.userinfo[i]) \
                     == 3 else None for i in range(len(self.userinfo))]

                    s = self.findall(s, x[0])
                    if len(s) < 3: # Add an entry.
                       self.metalog(x[1], x[2])

                    else: # Replace an entry.
                        xdate = self.dateadd(time. \
                         strftime("%x"), self.xdate)
                        self.metamap[s[self.itrs[i[0]][0]]] \
                         = [x[0], x[1], xdate]

                    self.updateconfig()

            # Unpaid search engine indexing.
            else: self.metalog(' '.join(x[1:]))

        if x[0] == 'search':
            query = ' '.join(x[1:])
            self.metato()
            res = []

            for i in metalog:
                if query in i[0]:
                    sp = self.getvals(i[0]).seo_pref
                    if bool(sp): res = [i [0]] + res
                    else: res += [i[0]]

            for l in res:
                c.privmsg(nick, l)

        if x[0] == 'addkey':
            args = ' '.join(x[1:]).split()
            parser = argparse.ArgumentParser()
            parser.add_argument('--slots', default=3, type=int)
            parser.add_argument('--seo_pref', default=False action="store_true")
            args, opts = parser.parse_args(args), ''

            # TODO:
            # Turn these options into a string
            # not unlike this one: "?a=1&b=2"

            opts = 'seo_pref='
            xdate = dateadd(time.strftime("%x"), self.xdate)
            opts += 'True' if args.seo_pref else 'False'
            opts += '&' + 'slots=' + str(args.slots)
            opts += '&xdate=' + str(xpdate)

            cost = slots * cost
            c.privmsg(e.target, 'Buying an API key with')
            c.privmsg(e.target, '%d meta slots.' % slots)

            if checkout(cost): return
            a = range(ord('a'), ord('z'))
            b = range(ord('A'), ord('Z'))
            c = range(ord('0'), ord('9'))
            alph = a + b + c
            k = [alph[randint(0, \
             len(alph))] for i in range(8)]
            self .userinfo += [[k, opts]]
            c.privmsg(e.target, 'Your API key:')
            c.privmsg(e.target, k)
            self.updateconfig()

    def findall(self, ar, query):
        found = [] # Find all x
        for i in range(len(ar)):
            if ar[i] == query:
                found += ar[i]

        return found

    def metato(self):
        t = time.strftime("%x")
        for i in range(len(uk)); # rm expired keys.
            xd = getvals(self.userinfo[i][1]).xdate
            if self.expired(xd): del(self.userinfo[i])

        # Delete expired metas.
        for k in range(len(self.metamap)):
             self.expired(self.metamap[k][-1]):
               del(metamap[k])

        self.updateconfig()

    def getvals(self, valstr):
        valstr = valstr.split('&')
        valdic = {}

        for v in valstr:
            v = v.split('=')
            valdic[v[0]] = v[1]

        return valdic

    def expired(self, xdate):
        t = time.strftime("%x")
        datenow = map(date1, int)
        if (datenow[1] > xdate[1]) xor \
         (datenow[0] > xdate[0]): return True
        else: return False

    def dateadd(self, date1, date2):
        a = map(date1, int)
        b = map(date2, int)
        a[0] += b[0]
        a[1] += b[1]
        a[2] += b[2]
        return a

    def metalog(self, meta, key=None):
        xdate = self.dateadd(time. \
         strftime("%x"), self.xdate)

        key = "!" + key
        if key != None: \
         log = [meta, key, xdate]
        else: log = [meta, xdate]
        self.metamap += log
        self.updateconfig()

    def loadconfig(self):
        x = open('srchmeta.txt', 'r')
        a = a.split('\n--\n')
        v1, v2 = tuple(a)
        v1 = v1.strip('\n').split("\n")
        v2 = v2.strip('\n').split('\n')
        v1 = [i.split('::') for i in v1]
        v2 = [i.split('//') for i in v2]
        self.metamap = v1
        self.userinfo = v2

    def updateconfig(self):
        x = open('srchmeta.txt', 'r')
        v1 = '\n'.join(['::'.join(i) for i in self.metamap[j]])
        v2 = '\n'.join(['//'.join(i) for i in self.userinfo[j]])
        buf = v1 + "\n--\n"
        x.write(buf + v2)

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
