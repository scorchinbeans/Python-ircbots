#! /usr/bin/env python
# (C) Paulus Madison Hay
# License: gplv2

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
from os import system
from bottle import route, run

class clibot(irc.bot.SingleServerIRCBot):
    def __init__(self, servport, uuid):
        nick, chan = _default_nickchan
        serv, port = servport

        irc.bot.SingleServerIRCBot.__init__(self, [(serv, port)], nick, nick)
        irc.client.ServerConnection.buffer_class.encoding = "latin-1"
        self.arcfn = uuid + '.zip'
        self.chanlog ={}
        self.chans = [ ]
        self.chan = chan
        self.serv = serv
        self.port = port
        self.uuid = uuid

    def on_join(self, c, e):
        self.chanlog[e.target] = ""

    def on_part(self, c, e):
        del(self.chanlog[e.target])

    # List results.
    def on_list(self, c, e):
        self.chans += [e.arguments[0]+"<br>"]

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.list()

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments[0])

    def on_pubmsg(self, c, e):
        self.chanlog[e.target] +="%s>> %s<br>" \
         % e.source.nick, e.arguments[0]

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
             (struct.pack("!I", data)

@route("/chatcli/<chan>")
def channel(chan):
    uuid = request.cookies.get("uuid", "0")
    nick = request.cookies.get("nick")
    chan = request.cookies.get("chan")

    if uuid == "0": # Cookie not found?
        uuid =gen_uuid() # Generate uuid.
        response.set_cookie("uuid", uuid)
        _bot[uuid] = clibot(default_servport, uuid)

    yield """<form action="#" onsubmit="sendmsg()" method="POST">
    <input type="text" name="msg" placeholder="the chat message">
    <input type="submit" value="Send"></form><br><div id="irclog">
    </div><script language="javascript">

    var Nick = """+nick+""";
    var Chan = """+chan+""";
    function loadFile(filePath) {
        var result = null;
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("GET", "/userfiles/" \
         + filePath, false);
        xmlhttp.send();

        if (xmlhttp.status == 200) {
        result = xmlhttp.responseText;
        }; return result;
    }

    function sendmsg() {
    var Msg = document.getElementById("msg");

    Msg = Msg.split(" ");
    if(Msg[0] == "/nick") {
        var chnick =Msg.splice(0, 1).join("_");
        document.cookie = "nick=" + chnick;
        return;
        }
    }

    # Must destroy irc bot once user leaves.
    window.onunload = function() {
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("GET", "/end, false);
        xmlhttp.send();
    }

    var data = {
     msg: Msg,
     nick: Nick
    };

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/sendmsg/"+chan, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(data));
    }

    function grablog() {
    document.getElementById("irclog")
    .innerHTML = loadFile("/chanlog/"
    +chan);}

    setInterval(grablog, 60000);
    </script>"""

@route("/endcli/")
def endcli():
    uuid = request.cookies.get("uuid")
    response.delete_cookie("uuid")
    response.delete_cookie("nick")
    response.delete_cookie("chan")
    remove(uuid + ".zip")
    del(_bot[uuid])

@route("/chanlog/<chan>")
def chanlog(chan):
    uuid = request.cookies.get("uuid")
    return _bot[uuid].chanlog[chan]

@route("/sendmsg/<chan>")
def sendmsg(chan):
    uuid = request.cookies.get("uuid")
    msg = request.forms.get("msg")
    nick = request.forms.get("nick")
    _bot[uuid].connection.privmsg(chan, \
     "%s>> %s" % (nick, msg))

@route("/userfiles/<fname>")
def user_files(username, fname):
    uuid = request.cookies.get("uuid")
    z = zipfile.ZipFile(uuid + ".zip", "r")
    return z.read(fname)
