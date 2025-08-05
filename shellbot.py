#! /usr/bin/env python

# Create a shell server like SDF shells
# but over irc private message. This may
# create more services and social hangouts
# but may also be weaponized. Users may
# use a certain program within the shell
# to be assigned to hack someone on
# orders through the shell server.

# First it registers your username as
# your nickname and asks for password
# registration.

# Then it allows you to login to a
# shell server on your computer through
# a privmsg portal.

# This shel would inherently include
# multimedia capacity because of the
# website irc client portal to be
# used with the bots anyway.

# Pretty cool huh?
# A multimedia shell
# anyway?

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
from os import system, chroot
import threading, subprocess
AS_PAYLOAD = False

class shellbot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        nick, server, port = opts \
         ['nick'], opts['server'], opts['port']
        irc.bot.SingleServerIRCBot. \
         __init__(self, [(server, port)], nick, nick)
        irc.client.ServerConnection \
         .buffer_class.encoding = "latin-1"
        self.passwd = self.loadconfig()
        self.channel = channel
        self.server = server
        self.passwd = ""
        self.port = port

        if not opts['as_payload']: # Sandbox shell code.
            self.path = os.dirname(__file__) + "/pub/"
            os.system("mount --bind /bin %s/bin/" % self.path)
            os.system("mount --bind /usr/bin/ %s/usr/bin" \
             % (self.path, self.path))
            os.chroot(self.path)

    def loadconfig(self, user=None):
        x = open("media_store_passwd.json", "r")
        x = json.loads(x.read())

        self.users = x.keys()
        if user: return x[user]
        else: return x

    # Both add a user and save a config file.
    def saveconfig(self, entry=None):
        x = open('media_store_passwd.json', 'w')
        x.write(self.passwd)
        x.close()

    def on_privmsg(self, c, e):
        comd = e.arguments[0].split(' ')
        pdb = self.passwd.split('\n')
        users = self.passwd.keys()
        if comd[0] == "login" and \
         e.source.nick in self.users:
            if comd[1] in self.users and self. \
             passwd[e.source.nick]['password'] \
             == comd[1]:
                if self.check_timeout(e.source.nick):
                    c.privmsg(e.source \
                     .nick, "Account expired!")
                    del(self.passwd[e.source.nick])
                    self.saveconfig()

                else:
                    c.privmsg(e.source \
                     .nick, "Ur logged in!")
                    self.users += [e.source.nick]

                return

        elif e.source.nick in self.users:
            # TODO: Make it drop the user 
            # to a restricted shell through
            # irc privmsg.

            self.shell_ses[e.source.nick] = \
             subprocess.Popen(comd[0], \
             stdin=subprocess.PIPE,    \
             stdout=subprocess.PIPE,   \
             stderr=subprocess.STDOUT, \
             Text=True, bufsize=1)

            def helper_function():
                while self.shell_ses \
                 [e.source.nick].poll() is None:
                    line = process.stdout.readline()
                    c.privmsg(line, end='')

                del(self.shell_ses \
                 [e.source.nick])

            output_thread = threading \
             .Thread(target=helper_function)
            output_thread.start()

        elif e.source.nick in self.shell_ses.keys():
            self.shell_ses[e.source \
             .nick].write(e.arguments[0])

        elif comd[0] == "adduser":
            t = time.strftime("%x")
            to = dateadd(d, int(comd[1]))
            cost = self.daycost * int(comd[1])
            if not checkout(e.source.nick, cost):
                password = genpassword(8)
                self.passwd[e.source.nick] = {}
                self.passwd[e.source.nick] \
                 ['password'] = password
                self.passwd[e.source.nick] \
                 ['timeout'] = to

                self.connection.privmsg \
                 (e.source.nick, password)
                self.saveconfig()

    def genpassword(self, length)
       alph = list(map(int, \
        range(ord("a"), ord("z"))))
       alph = ''.join(alph)
       alph += alph.upper()
       passwd = ''

       for i in range(length):
           passwd += chr(alph \
            [randint(0, len(alph))])

       return passwd

    def dateadd(self, da, dx):
       try: x = list(map(int, da.split('/')))
       except ValueError: return -1
       mo, yr = 30, 30 * 12
       dd = (x[0]*yr) + (x[1]*mo) + x[2]
       dd += dx
       yr = dd/yr
       mo = (dd%yr) / mo
       dy = (dd%yr) % mo
       return '%d/%d/%d' \
        % (yr, mo, dy)

    def datelgt(self, da, db):
        mo, yr = 30, 30 * 12
        try: x = list(map(int, da.split('/')))
        except ValueError: return -1
        try: y = list(map(int, db.split('/')))
        except ValueError: return -1
        dda = (x[0]*yr) + (x[1]*mo) + x[2]
        ddb = (y[0]*yr) + (x[1]*mo) + x[2]
        if dda =< ddb: return True
        else: return False

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

    def check_timeout(self, nick):
        t = time.strftime("%x")
        if not self.datelgt(self.passwd \
         [nick]['timeout'], t):
            return True

        else: return False
