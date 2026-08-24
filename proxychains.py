#! /usr/bin/env python
# Create an application which act as either an entrance
# node, a continuance node, or an exit node. An entrance
# node accepts a connection from the internet, then it
# relays that between continuance nodes, then the exit
# node relays that connection from a conuance to a
# connection into the internet.

# So when a user pm's any one of these nodes
# it will circulate that nick wants the proxy
# chain in that order:

# Circulated file:
# [nickname]|[node 1]/[node 2]/[target]:[port]

# Each node will store this chains
# file until the nickname !pms any
# bot to cancel the chain, then
# they circulate the cancel
# [nick] signal to all bots
# in the chain.

# Once the connection and routing
# is set up that way, use a seperate
# local side bot script to route
# sockets to DCC connections.

# TODO:
# Try making the chain behave
# like a SOCKS proxy using:
# https://github.com/MisterDaneel/pysoxy

# The current state of its 
# operational security...

# That this device makes the users
# of its network so much money, people
# who use it may be expected to have
# many lawyers readily perhaps to
# defend themselves and each other
# from criminal charges and lawsuits.

# Their money may be under watch
# by the american SEC, for their
# money's complicity with criminal
# and targeted organizations. Such
# alledgibility and culpability
# have been mitigated by license.
# But user beware!

# Maybe use a link to this page
# to blame trump for communist
# complicity in his slanderous
# criminal trials and suits.

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
from bot_boilerplate import boilerplate
from os import system
mainclass = "TestBot"

class TestBot(boilerplate):
    def bot_init(self, opts):
        nick, server, port = opts['nick'], opts['server'], opts['port']
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nick, nick)
        irc.client.ServerConnection.buffer_class.encoding = "latin-1"
        self.channel = channel
        self.server = server
        self.port = port
        self.nodecost = 5

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_privmsg(self, c, e):
        cmd = e.arguments[0].split(' ')
        nick = e.source.nick

        if cmd[0] == 'help':
            for i in userhelp.split('\n'):
                c.privmsg(nick, i)

        elif cmd[0] == 'circ-chain':
            chain = [cmd[1]]
            self.checkout(nick, self.nodecost)
            lasthost = chain.split('/') [-1]
            lastnode = chain.split('/') [-2]
            firstnode = chain.split('/') [0]
            lasthost = lasthost.split (':')
            src_nick = chain.split('|') [0]
            self.chains += [chain]

            if self.get_nickname() == lastnode:
                # Open the exit node client socket.
                self.exit_sock[src_nick] = socket. \
                 socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((lasthost[0], lasthost[1]))
                Thread(target=self.exit_recv_thread, \
                 args=(src_nick,))

            elif self.get_nickname() == firstnode:
                self.entry_sock[src_nick] = socket \
                 .socket(socket.AF_INT, socket.SOCK_STREAM)
                try: self.entry_sock[src_nick].bind(('', lasthost[1]))
                except socket.error as msg:
                    c.privmsg(src_nick, "Bind failed")
                    return

                s.listen(10)
                conn, addr = s.accept()
                sock.connect((lasthost[0], lasthost[1]))
                Thread(target=self.entry_recv_thread, \
                 args=(src_nick,))

        elif cmd[0] == 'add-chain':
            chain = '/'.join(cmd[1:])
            nodes = chain.split('/')[:-1]
            chain = nick + '|' + chain
            self.chains += [chain]

            # Circulate chain to other
            # nodes involved.

            for node in nodes:
                c.privmsg(node, \
                 'circ-chain ' + chain)

    def exit_recv_thread(self, srcnick):
        self.exit_sock[srcnick].recv(1024)
        cnicks = [i.split('|')[0] for i in self.chains]
        chain = self.chains[cnicks.index(srcnick)]
        lastnode = chain .split ('/') [-2]
        self.send_file(dat, lastnode, srcnick)

    def entry_recv_thread(self, srcnick):
        self.exit_sock[srcnick].recv(1024)
        cnicks = [i.split('|')[0] for i in self.chains]
        chain = self.chains[cnicks.index(srcnick)]
        firstnode = chain .split ('/') [1]
        self.send_file(dat, firstnode, srcnick)

    # cnick is the original nickname
    # of the irc user who set up the
    # proxy chain, and the name of
    # the proxy chain.

    def send_file(self, opr_data, reciever, cnick):
        self.dcc += [self.dcc_listen("raw")]
        filesize = os.path.getsize(filename)
        msg_parts = map(
            str,
            (
                'SEND', cnick,
                os.path.basename(filename),
                irc.client.ip_quad_to_numstr \
                 (self.dcc[-1].localaddress),
                self.dcc[-1].localport,
                filesize,
            ),
        )

        self.ustreams += [opr_data]
        msg = subprocess.list2cmdline(msg_parts)
        self.connection.ctcp("DCC", receiver, msg)
        if filesize != 0: self.dcc[-1] \
         .send_bytes(ustreams[-1][:1024])

    # Message recieved
    def on_ctcp(self, connection, event):
        payload = event.arguments[1]
        parts = shlex.split(payload)
        command, cnick, filename, peer_address, \
         peer_port, size = parts
        if command != "SEND":
            return

        rnick = e.source.nick
        self.rcnick[rnick] = cnick
        if rnick in self.dstream.keys():
            connection.privmsg(rnick, \
             "Still Recieving file.")
            return

        self.filename[rnick] = \
         os.path.basename(filename)

        if os.path.exists(self.filename[rnick]):
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
                cnicks = [i.split('|')[0] for i in self.chains]
                Ichain = cnicks .index(self.rcnick[rnick])
                chain = self.chains[Ichain].split('|')[1:]
                chain = '|' .join(chain)
                chain = chain.split('/')

                me = chain.index(c.get_nickname())
                src = chains[cnicks[Ichain]] .index (rnick)
                one = cnicks[Ichain]

                step = me + (src - me)
                dest = self.chains [step]
                self.send_file(dest, \
                 self.dstream[rnick])

                # last node in the chain.
                if one in self.exit_sock \
                 .keys() and src - me < 0:
                    self.exit_sock.send(dstream [rnick])

                elif one in self.entry_sock \
                 .keys() and (src - me) > 0:
                    self.entry_sock.send(dstream [rnick])

                del(self.filename    [rnick])
                del(self.dstream     [rnick])
                del(self.rfsize      [rnick])
                del(self.rdcc        [rnick])
                return

            self.dstream[rnick] += data
            self.rdcc[rnick].send_bytes \
             (struct.pack("!I", data))

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
    
    def cmd_parser(self, e, cmd):
        nick = e.source.nick
        c = self.connection

        if cmd == "disconnect":
            self.disconnect()

        elif cmd == "die":
            self.die()

        elif cmd == "stats":
            for chname, chobj in self.channels.items():
                c.notice(nick, "--- Channel statistics ---")
                c.notice(nick, "Channel: " + chname)
                users = sorted(chobj.users())
                c.notice(nick, "Users: " + ", ".join(users))
                opers = sorted(chobj.opers())
                c.notice(nick, "Opers: " + ", ".join(opers))
                voiced = sorted(chobj.voiced())
                c.notice(nick, "Voiced: " + ", ".join(voiced))

        elif cmd == "dcc":
            dcc = self.dcc_listen()
            c.ctcp(
                "DCC",
                nick,
                f"CHAT chat {ip_quad_to_numstr(dcc.localaddress)} {dcc.localport}",
            )

        else:
            c.notice(nick, "Not understood: " + cmd)
