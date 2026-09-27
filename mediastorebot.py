# (C) Paulus Madison Hay
# Media storage  robot which
# stores media

# TODO:
# Make it forward profits
# to the file sellers.

import argparse
import os
import struct
import subprocess
import sys

import jaraco.logging
import irc.client
import re

class clibot(irc.bot.SingleServerIRCBot):
    def startbot(self, opts):
        nick, server, port = \
         opts['nick'], \
         opts['server'], \
         opts['port']

        self.channel = channel
        self.server  = server
        self.listend = False
        self.port  = port
        self.chanlog = {}
        self.chans = []
        self.users = []
        self.gb = 1024
        self.tb \
         = gb * 1024

    def on_join(self, c, e):
        self.chanlog[e.target] = ""
        self.chans += [e.target]

    def on_part(self, c, e):
        if e.target not in self.chans: return
        del(self.chans[self.chans.index(e.target)])
        del(self.chanlog[e.target])

    def on_listend(self, c, e):
        self.listend = True

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def bot_welcome(self, c, e):
        c.list()

    def send_file(self, filename, reciever):
        self.dcc += [self.dcc_listen("raw")]
        filesize = os.path.getsize(filename)
        msg_parts = map(
            str,
            (
                'SEND',
                os.path.basename(filename),
                irc.client.ip_quad_to_numstr \
                 (self.dcc[-1].localaddress),
                self.dcc[-1].localport,
                filesize,
            ),
        )

        f = ZipFile.open (self.arcfn, 'rb')
        self.ustreams += [f.read(filename)]
        self.connection.privmsg(reciever, \
         "Sending " + filename) # Notify user
        msg = subprocess.list2cmdline(msg_parts)
        self.connection.ctcp("DCC", receiver, msg)
        if filesize != 0: self.dcc[-1] \
         .send_bytes(ustreams[-1][:1024])

    # Message recieved
    def on_ctcp(self, connection, event):
        payload = event.arguments[1]
        parts = shlex.split(payload)
        command, filename, peer_address, \
         peer_port, size = parts
        if command != "SEND":
            return

        rnick = e.source.nick
        if rnick in self.dstream.keys():
            connection.privmsg(rnick, \
             "Still Recieving file.")
            return

        self.filename[rnick] = \
         os.path.basename(filename)

        if os.path.exists(self.filename):
            print("A file named", self.filename, \
             "already exists. Refusing to save it.")
            self.connection.quit()
            return

        self.dstream[rnick] = ""
        self.rfsize[rnick] = parts[4]
        peer_address = irc.client. \
         ip_numstr_to_quad(peer_address)
        peer_port = int(peer_port)
        self.rdcc[rnick] = self.dcc_connect \
         (peer_address, peer_port, "raw")

    def on_dccmsg(self, connection, event):
        item_found, acked = False, struct \
         .unpack("!I", event.arguments[0])[0]
        for stream in range(len(self.ustreams)):
            if acked in self.ustreams[stream]:
                self.ustreams [stream] = \
                 self.ustreams[stream][1024:]
                item_found = True
                break

        rnick = event.source.nick
        if item_found: # Finished sending.
            if len(ustreams[stream]) == 0:
                self.dcc[stream].disconnect()
                del(self.ustreams[stream])
                del(self.dcc[stream])

            else: # Send data.
                data = self.ustreams[stream][:1024]
                self.dcc[stream].send_bytes(data)

        else: # Recieve data
            rnick = event.source.nick
            data = event.arguments[0]
            if len(self.dstream[rnick]) \
             + len(data) == self.rfsize[rnick]:
                c.privmsg(rnick, \ # Notify user
                 "Recieved " + self.filename)
                i = ZipFile.open(self.arcfn, "wb")
                i.writestr(self.filename, self.dstream[rnick])
                i.close() # Write the file to local fs.

                del(self.filename    [rnick])
                del(self.dstream     [rnick])
                del(self.rfsize      [rnick])
                del(self.rdcc        [rnick])
                return

            self.dstream[rnick] += data
            self.rdcc[rnick].send_bytes \
             (struct.pack("!I", data))

    def loadconfig(self, user=None):
        x = open("media_store_passwd.json", "r")
        self.passwd = json.loads(x.read())
        self.users = self.passwd.keys()
        return passwd

    # Both add a user and save a config file.
    def saveconfig(self, entry=None):
        x = open('media_store_passwd.json', 'w')
        x.write(json.dumps(self.passwd))
        x.close()

    def on_privmsg(self, c, e):
        comd = e.arguments [0]
        nick = e. source. nick
        comd = comd.split(' ')
        if comd[0] == 'login':
            login = entry(nick)
            if not login: return
            if comd[1] == login[1]:
                self.users += [nick]
                return

        elif comd[0] == "logout":
            del(self.users[self.users.index(nick)])

        elif comd[0] == "register":
            paswd = comd[1]
            storg = comd[2]
            # User entry: [passwd, xdate, profit]
            xdate = self.add_date(time \
             .strftime("%x"), int(comd[3]))
            entry = [passwd, xdate, 0]
            if nick not in self.passwd.keys():
                unit = re.findall("[a-zA-Z]+", storg)[0]
                size = int(re.findall("[0-9]+", storg))[0]
                if unit == "gb": size = size * self.gb
                elif unit == "tb": size = size * self.tb
                if not checkout(nick, size * self.cost * month):
                    x = ZipFile.open(nick + ".zip", "w")
                    self.passwd[nick]['password'] = passwd
                    self.passwd[nick]['xdate'] = xdate
                    self.passwd[nick]['profit'] = 0
                    self.saveconfig()
                    x.close()

        if nick in self.users:
            if comd[0] == "dir":
                if len(comd) == 1: comd += ['.']
                z = ZipFile.open(nick + '.zip', 'r')
                c.privmsg(nick, "Dir listing for %s" % comd[1])
                for f in z.namelist(): c.privmsg(nick, f)

            elif comd[0] == "get":
                self.send_file(comd[1], nick)

            # Mark file as for sale.
            elif comd[0] == "sell":
                Z = zipfile.ZipFile \
                 (nick + '.zip', 'r')
                z = json.loads(Z.open \
                 ('config.json').read())

                z[comd[1]] = {}
                z[comd[1]]['price'] \
                 = comd[2] # path, cost

                Z = zipfile.ZipFile \
                 (nick + '.zip', 'w')
                zz = Z.open('config.json')
                zz.write(json.dumps(z))
                z.close()

            elif comd[0] == "cashout":
                btcaddr = comd[1]
                x = self.passwd[e.source.nick]
                profit = int(x['profit'])
                self.passwd[e.source.nick] \
                 ['profit'] = "0"

                profit = profit * 0.30
                system("electrum payto %s %s" \
                 % (btcaddr, profit))
                self.saveconfig()

        if comd[0] == "buy":
            bnick = comd[1]
            bpath, res = comd[2], False
            zf = zipfile.ZipFile \
             (bnick + ".zip", 'r')
            d = json.loads(zf.open \
             ('/config.json').read())
            cost = d[bpath]['price']

            if !self.checkout(nick, cost)
                self.send_file(bpath, bnick)
                pusers = self .passwd.keys()
                self.passwd[nick]['profit'] += cost
                self.saveconfig()

        if comd[0] == "list-forsale":
            bnick = comd[1] # List files for sale
            zipfile.ZipFile(bnick + ".zip", 'r')
            z = zz.open("config.json")
            d = json.loads(z.read())

            for f in d.keys():
                c.privmsg(e.source.nick, \
                 f + ' ' + str(d[f]['price'])

        if comd[0] == "help":
            c.privmsg(nick, "mediastorebot help.")
            c.privmsg(nick, "--- if logged in ---")
            c.privmsg(nick, " ")

            c.privmsg(nick, "dir [path]")
            c.privmsg(nick, "List files in directoy [dir]")
            c.privmsg(nick, " ")

            c.privmsg(nick, "get [path]")
            c.privmsg(nick, "Download the file at [path]")
            c.privmsg(nick, " ")

            c.privmsg(nick, "sell [file] [price]")
            c.privmsg(nick, "Mark [file] for sale")
            c.privmsg(nick, "for [price] btc.")
            c.privmsg(nick, " ")

            c.privmsg(nick, "cashout [btcaddr]")
            c.privmsg(nick, "Recieve your profits")
            c.privmsg(nick, "to [btcaddr]")
            c.privmsg(nick, " ")

            c.privmsg(nick, "--- If logged out ---")
            c.privmsg(nick, "buy [user] [file_path]")
            c.privmsg(nick, "Buy the file by its path")
            c.privmsg(nick, "from the user [user]")
            c.privmsg(nick, " ")

            c.privmsg(nick, "list-forsale [user]")
            c.privmsg(nick, "List the user's files for sale")
            c.privmsg(nick, " ")

            c.privmsg(nick, "Profit-store [mbs]"
            c.privmsg(nick, "Store some offloaded files")
            c.privmsg(nick, "on your browser for money.")
            c.privmsg(nick, " ")

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

    def expired(self, xdate):
        tnow = time.strftime("%x")
        datenow = list(map (int, tnow))
        xdate = list(map(int, xdate))
        mo = 30
        yr = mo * 12
        dd = (datenow[0] * yr) \
         + (datenow[1] * mo) \
         + datenow[2]

        dx = (xdate[0] * yr) \
         + (xdate[1] * mo) \
         + xdate[2]

        if dd => dx: return True
        else: return False
