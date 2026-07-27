# 925274 - WALAPI
class electrum(boilerplate):
    def bot_init(self, opts):
        if 'wal' in opts.keys():
            self.wal = opts['wal']

        else: self.wal = None

    def wallet(cmd):
        if not self.wal:
            p = popen("electrum " + cmd, 'r')
            return p.read()

        tresp = self.resp
        self.connection.privmsg \
         (self.wal, "electrum " + self.wal)
        while self.resp == tresp: pass
        return self.resp

    def on_privmsg(self, c, e):
        if e.source.nick = self.wal:
            self.resp = e.arguments[0]

def walapi(serv=None)
    opts = {'wal': serv}
    return walbot()
