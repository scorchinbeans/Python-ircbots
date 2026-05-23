import irc.bot
import irc.strings
from irc.client import \
 ip_numstr_to_quad, ip_quad_to_numstr
from bot_boilerplate import boilerplate
from os import system, popen
import schedule

mainclass = 'smsbot'
password = "botnet"
class smsbot(boilerplate):
    def bot_init(self, opts):
        nick, server, port = opts['nick'], opts['server'], opts['port']
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nick, nick)
        irc.client.ServerConnection.buffer_class.encoding = "latin-1"
        self.channel = channel
        self.server  = server
        self.authnr  = False
        self.port    = port
        x = []

        for i in range(20):
            x[i] = smsbot(boilerplate)

    def chkauth(self):
        x = popen('termux-sms-list -l 30', 'r')
        authlist = json.loads(x.read())
        for i in authlist[::-1]:
            if i.message == password:
                self.authnr = i.address
                system('termux-sms-send -n %s ' \
                 + 'Welcome to the neon saturn' \
                 + ' botnet!' % self.authnr
                break

    def chksms(self):
        if not self.authnr: return
        x = popen('termux-sms-list -l 5', 'r')
        self.smslist = json.loads(x.read())

        bbcue = []
        for i in self.smslist:
            if i.adress == self.authnr:
                bbcue = i.message

        for i in bbcue:
            chan = self.chan
            ii = i.split(' ')
            msg = i

            elif ii[0] == '/join':
                self.join(ii[1])
                break

            elif ii[0] == '/nick':
                self.nick = ii[1]
                break

            else:
                if ii[0] == '/pm':
                     msg = ' '.join(ii[2:])
                     chan = ii[1]

                self.connection \
                 .privmsg(chan, msg)

    def on_join(self, c, e):
        self.part(self.chan)
        self.chan = e.target

    def bot_welcome(self, c, e):
        schedule.every(30). \
         seconds.do(self.chkauth)
        schedule.every(05). \
         seconds.do(self.chksms)

    def on_privmsg(self, c, e):
        src = e.source.nick + ': '
        msg = src + e.arguments[0]
        if not self.authnr: return
        system('termux-sms-send -n %s %s' \
         % (self.authnr, msg))

    def on_pubmsg(self, c, e):
        if not self.authnr: return
        system('termux-sms-send -n %s %s' \
         % (self.authnr, e.arguments[0]))
