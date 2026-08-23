# (C) Paulus Madison Hay
# License: gplv3

import ssl, functools
import irc.bot, irc.client
class boilerplate(irc.bot.SingleServerIRCBot):
    def __init__(self, opers):
        self.status = {} # Boilerplate.
        irc.client.ServerConnection. \
         buffer_class.encoding = "latin-1"
        conn = (opers['server'], opers['port'])
        irc.bot.SingleServerIRCBot.__init__(self, \
         [conn], opers['nick'], opers['nick'])
        self.status['session-begin'] = False
        self.status['bot-init'] = True
        self.opers = opers

        if opers['ssl']: # Setup SSL.
            cnt = ssl.create_default_context()
            wrapper = functools.partial(cnt.wrap_socket, \
             server_hostname = opers['server'])

            self.connect(opers['server'], opers['port'], \
             opers['nick'], None, connect_factory = \
             irc.connection.Factory(wrapper=wrapper))

        # Run bot_init if existing.
        try: self.bot_init(opers)
        except NameError: pass

    def on_welcome(self, c, e):
        self.status['session-begin'] = True
        # Run bot_welcome if it's existing.
        try: self.bot_welcome(c, e)
        except NameError: pass

    def do_command(self, cmd):
        cmd = cmd.split(' ')
        if cmd[0] == "join":
            self.connection.join(cmd[1])

        elif cmd[0] == "part":
            self.connection.part(cmd[1])

        # Forward to child class.
        try: self.cmd_parser(cmd)
        except NameError: pass
