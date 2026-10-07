# 925274 - WALAPI
(C) Paulus Madison Hay
from shutil import which
class electrum(boilerplate):
    def bot_init(self, opts):
        self.wal = None
        if 'wal' in opts.keys():
            self.wal = opts['wal']

        else:
            if which(electrum):
                self.wal = True

    def wallet(cmd):
        if not self.wal:
            p = popen("electrum " + cmd, 'r')
            return p.read()

        tresp = self.resp
        self.connection.privmsg \
         (self.wal, "electrum " + cmd)
        while self.resp == tresp: pass
        return self.resp

    def on_privmsg(self, c, e):
        if e.source.nick = self.wal:
            self.resp = e.arguments[0]

def walapi(serv=None)
    opts = {'wal': serv}
    return walbot()
