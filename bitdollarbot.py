# (C) Paulus Madison Hay
# on: august 8 2024
# License: gplv3

# Bitvouchers are like a reserve
# currency system. People put in bitcoins
# and get out bitcoins. Right now its like
# a checking system where money is deposited
# into the reserve and withdrawn according
# to the bill hash. Ideally, and without
# tampering, each bill's value directly
# cooresponds to a constant number of
# bitcoins in the reserve.

# If someone captured the bill's code,
# they could steal its value from under
# your vault.

# Decline of the currency: If the number
# of bitcoins cooresponding to the same
# bill value in the reserve decreases,
# or increases, the currency becomes
# worth less or more.

# Unless you loan money from the reserve
# system, and decrease the value of each
# dollar as you do so (like inflation)
# then the currency becomes worthless
# eventually anyway.

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
from bot_boilerplate import boilerplate
from os import system, popen
from time import strftime
mainclass = 'bitdollarbot'
import json
import rsa

class bitdollarbot(boilerplate):
    def bot_init(self, opers):
        self.sfile = "settings.json"
        self.server = opers['server']
        self.port = opers['port']
        self.channel = channel
        self.started = False
        self.secprompt ={}
        self.tmp_vval = {}
        self.vouchers = []
        self.traffic = {}

        xrate = 0.00001827
        self.Vcost = xrate * 3

        # Generate voucher file.
        if not exists(self.sfile):
            self.pubkey, self.privkey = rsa.newkeys(512)
            self.update_settings_file()

        else: # Read voucher file.
            x = open(self.sfile, "r")
            x = json.loads( x.read( ) )
            self.vouchers += x['vouchers']
            self.privkey = x['privkey']
            self.pubkey =  x['pubkey']


    # Mode: True if logging a voucher issuance
    # and false if logging a voucher redeeming.
    def log_voucher(mode, bill, adress):
        t = strftime("%x") # Time of.
        x = open("voucherlog.txt", "a")
        m = 'ISSUED' if mode else "REDEEMED"
        y = '%s//%s//%s//%s\n' % (m, bill, adress, t)
        x.write(y)
        x.close()

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_join(self, c, e):
        self.traffic[chan] = 0
        c.privmsg(e.target, "Bitvoucher bot \
         here! pm me !help for instructions.")

    def on_privmsg(self, c, e):
        nick = e.source.nick
        cmd = e.arguments[0].split(' ')
        if nick in self.secprompt.keys():
            if self.secprompt[nick] == "cashvoucher":
                tmp_addr = cmd[1] # Redeem a voucher.
                amt = self.tmp_vval[nick]

                self.log_voucher(self.tmp_voucher, tmp_adress)
                c.privmsg(nick, "Redeeming your bitcoins.")
                c.privmsg(nick, "paying to: " + tmp_adress)
                system("electrum payto %s %f" % \
                 (tmp_addr[nick], amt))

                del(self.tmp_voucher)
                del(self.tmp_vval[nick])
                del(self.secprompt[nick])

        if cmd[0] == "!check-voucher":
            voucher = self.checkvoucher(cmd[1])
            if not voucher:
                c.privmsg("Invalid voucher!")
                c.privmsg("We could not locate a voucher")
                c.privmsg("by this signature in our records ")
                c.privmsg("It may be forged or double-spent.")
                return

            else:
                v = tuple(voucher) # Describe the bill.
                c.privmsg("Voucher no. %d confirmed.  " % v[0])
                c.privmsg("Redeemable bitcoins found: " + v[1])
                return

        if cmd[0] == "!cash-voucher":
            if checkout:
                c.privmsg(nick, \
                 "Must pay to redeem bitdollars!")
                return

             self.tmp_voucher = self. \
             checkvoucher(cmd[1])

            if self.tmp_voucher == 0:
                c.privmsg(nick, "Could not confirm your voucher.")
                c.privmsg(nick, "serial. Its probably forged or")
                c.privmsg(nick, "or double-spent.")
                return

            if self.find_ds(cmd[1]):
                c.privmsg(nick, "Double spending detected! \
                 This money has already been redeemed and  \
                 now is worthless. Maybe someone copied it.")

            v = tuple(self.tmp_voucher)
            c.privmsg(nick, "Voucher no. %d confirmed.  " % v[0])
            c.privmsg(nick, "Redeemable bitcoins found: " + v[1])
            c.privmsg(nick, "PM me your bitcoin adress: ")
            self.secprompt[nick] = "cashvoucher"
            self.tmp_vval[nick] = v[1]
            return

        if cmd[0] == "!create-voucher":
            charge = float(cmd[1]) + \
             (float(cmd[1]) * self.Vcost)
            if not self.checkout(nick, charge):
                c.privmsg("Payment failed. Bailing out.")
                return

            sig = self.genvoucher(float(cmd[1]))
            c.privmsg(nick, "Generated your voucher.")
            c.privmsg(nick, "Your voucher serial is:")
            c.privmsg(nick, " ") # Formatting spacer
            c.privmsg(nick, sig) # show voucher serial
            c.privmsg(nick, "Enter this \
             serial when redeeming voucher.")
            c.privmsg("DCC sending bill image \
             for printing at home.")

        if cmd[0] == "!help":
            c.privmsg(nick, "!create-voucher [value]")
            c.privmsg(nick, "Creates a voucher redeemable")
            c.privmsg(nick, "here for [value] bitcoins.")
            c.privmsg(nick, " ")
            c.privmsg(nick, "!cash-voucher [voucher serial]")
            c.privmsg(nick, "Redeems bitcoin voucher to your")
            c.privmsg(nick, "provided adress.")
            c.privmsg(nick, " ")
            c.privmsg(nick, "Notes:")
            c.privmsg(nick, "Adding a 30% charge over")
            c.privmsg(nick, "value of voucher total to")
            c.privmsg(nick, "create a voucher and to")
            c.privmsg(nick, "redeem a voucher.")

    def on_pubmsg(self, c, e):
        nick = e.source.nick
        chan = e.target

        if not self.traffic[chan] % 10:
            c.privmsg(nick, "I am bitvoucher bot. \
             pm me !help for instructions.")

        self.traffic[chan] += 1

    def genvoucher(self, val):
        x = range(ord('a'), ord('z'))
        salt = [x[randint(0, len(x))] \
         for i in range(8)]

        voucher = str(len(vouchers)).rjust(4, "0")
        voucher += "/" + str(val) + '/' + salt

        hash = rsa.compute_hash(voucher, "SHA-1")
        sig = rsa.sign_hash(hash, self.privkey, "SHA-1")
        self.vouchers += [voucher]
        self.update_data_file()
        return base64.b64encode(sig)

    def checkvoucher(self, code):
        code = base64.b64decode(code)
        for voucher in self.vouchers:
            try: res = rsa.verify(voucher, code, self.pubkey)
            except rsa.pkcs1.VerificationError:
                if voucher == self.vouchers[-1]: return 0
                continue

            else: break

        res = map(int, voucher.split('/'))
        return res

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

    def update_data_file(self):
        dat = {"pubkey":self.pubkey,
         "privkey": self.privkey,
         "vouchers": self.vouchers}

        x = open("settings.json", "w")
        x.write(json.dumps(dat))
        x.close()

    def cmd_parser(self, cmd):
        cmd = cmd.split(' ')

        # /!\ Currency manipulation!
        # The currency is based on a fractional reserve
        # currency system. When you create a "free" bill
        # you are borrowing against the failure of that
        # currency, the last money cashed from
        # circulation.

        # /!\ Counterfeit warning!
        # If the private key is stolen from your vault,
        # new currency may be issued by the hacker and
        # his friends if distributed if they make a new
        # signed hash of a forged entry in the database
        # and printing them, they may be redeemed
        # fraudulently by stealing some money from
        # the failure of the currency.

        if cmd[0] == "free-false-voucher":
            sig = self.genvoucher(float(cmd[1]))
            print(sig)

        # Prints the server operator extra coins
        # which they pay for without an extra fee.

        elif cmd[0] == "gratis-voucher":
            val = cmd[1]
            if not checkout("self", val):
                sig = self.genvoucher(float(val))
                print(sig)

        # If the currency was copied, trace_dslog
        # will find duplicate spendings of any bill
        # and report them to the user.

        if cmd[0] == "trace_dslog":
            x = open('voucherlog.txt', 'r')
            x, xx =x.read().split('\n'), []
            print("double-spendings found:")
            for y in x:
                y = y.split('//')
                if y[1] in xx:
                   print(''.join(y[1]))

                xx += \
                 [y[1]]
