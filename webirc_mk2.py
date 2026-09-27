#! /usr/bin/env python
# (C) Paulus Madison Hay

# The bottle IRC server.
# This one will try to incorporate brython to
# approximate mk2's capabilities in the client
# side without incorporating the socket or irc
# module in brython.

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
from bot_boilerplate import boilerplate
from os import system, remove
from bottle import route, run
mainclass = 'webirc'

class clibot(irc.bot.SingleServerIRCBot):
    def __init__(self, servport, stats={}):
        if not stats: return
        nick = stats['nick']
        chan = stats['chan']
        uuid = stats['uuid']
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
        self.nick = nick

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
        if event.arguments[0] == "VERSION":
            connection.send_notice \
             (self.nick, "Just probed.")
            connection.ctcp_reply(event \
             .source.nick, "VERSION", \
             "webirc mk1.1")

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
                 self.ustreams[stream].pop(1024)
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
                c.privmsg(rnick, # Notify user \
                 "Recieved " + self.filename)
                i = ZipFile.open(self.arcfn, "wb")
                i.writestr(self.filename, self.dstream[rnick])
                i.close() # Write the file to local fs.

                del(self.filename [rnick])
                del(self.dstream  [rnick])
                del(self.rfsize   [rnick])
                del(self.rdcc     [rnick])
                return

            self.dstream[rnick] += data
            self.rdcc[rnick].send_bytes \
             (struct.pack("!I", data))

class webirc(irc.bot.SingleServerIRCBot):
    def __init__(self, opts):
        _default_port = opts['port']
        _default_serv = opts['server']
        ind = _default_serv.split('.')
        wport = opts['webport']
        self.status = {}

        ind = _default_serv.split('.')
        del(ind[0])
        del(ind[1])

        ind = '.'.join(ind)
        _servers[ind] =   \
         [(_default_serv, \
         _default_port)]

        if not wport: wport = 8080
        run(host="localhost", port=wport, quiet=True)
        self.status['bot-init'] = True

    def do_command(self, cmd):
        cmd = cmd.split(' ')
        if cmd[0] == "add_irc_server":
            serv = (cmd[1], cmd[2])
            ind = cmd[1].split('.')
            del(ind[0])
            del(ind[1])

            ind = '.'.join(ind)
            _servers += [serv]

@route("/chatcli/<addr>")
def channel(addr):
    if addr:
        chan, serv = addr.split('@')
        serv = _servers[serv]
        chan = "#" + chan

    else:
        serv = _default_serv
        chan = _default_chan

    print("breakpoint")
    uuid = request.cookies.get("uuid", "0")
    if uuid == "0": # Cookie not found?
        uuid = gen_uuid() # Generate uuid.
        nick = new_user() # Generate nick.
        response.set_cookie("uuid", uuid)
        response.set_cookie("nick", nick)
        response.set_cookie("chan", chan)
        stats = {'uuid': uuid, 'nick': nick, 'chan': chan}
        _bot[uuid] = clibot (serv, stats)

    yield """<head><meta charset="utf-8">
    <script type="text/javascript" src="brython.js"></script>
    <script type="text/javascript" src="brython_stdlib.js"></script>

    </head><br><dialog id="ide">
    <table cols=2 rows=3 border="0px"><tr>
    <td> <button onclick="ide_save()">Save
    file</button></td><td rowspan="3">

    <textarea id="botcode"
    placeholder="Your bot's code!"
    rows="3" cols="60"></textarea>
    </td></tr>

    <tr><td><select onchange="ide_load(this);"
    onload="ide_fillopts(this)"></select></tr>
    </td><tr><td><button onclick="ide_run();">
    Run </button> </tr> </td></table></dialog>

    <body onload="brython(1)">
    <button onclick="document.
    getElementById("ide").show( );">
    Show IDE</button><div id="tabs">
    <a href="#" onclick="swtab(this)" name="
    """ + chan + ">" + chan +  """</a></div>
    <form action="#" onsubmit="sendmsg()" method="POST">
    <input type="text" name="msg" placeholder="the chat message:">
    <input type="submit" value="Send"></form><br><div id="irclog">
    </div></body><script language="text/javascript">
    var Nick = getCookie("nick");
    var Chan = getCookie("chan");
    var irclog = {Chan: ""};
    var curbot = '';

    function ide_fillopts(selbox) {
        o = document.createElement('option')
        o.textContent = "new"
        o.value = "new"
        selbox .add (o)

        for i in Object.keys(bots) {
            o = document.createElement('option')
            o.textContent = i
            o.value = i
            selbox.add(o)
        }
    }

    function getCookie(name) {
        const value = '; ${document.cookie}';
        const parts = value.split('; ${name}=');
        if(parts.length === 2) return parts.
        pop().split(';').shift();
        return null;
    }

    function loadFile(filePath) {
        var result = null;
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("GET", filePath, false);
        xmlhttp.send();

        if (xmlhttp.status == 200) {
        result = xmlhttp.responseText;
        }; return result;
    }

    function sendmsg() {
        var Msg = document
        .getElementById("msg");

        Msg = Msg.split(" ");
        if(Msg[0] == "/nick") {
            var chnick = Msg.splice(0, 1).join("_");
            document.cookie = "nick=" + chnick;
            return;
            }

        if(Msg[0] == "/files") {
            var f = loadFile("/listfiles/")
            document.getElementById("irclog")
            .innerHTML += f
            }

        if(Msg[0] == "/join" and !Object
        .keys(irclog).includes(Msg[1])) {
            document.getElementById("tabs").innerHTML
            += '<a href="#" onclick="swtab(this)"
            name="' + Msg[1] + '">' + Msg[1]
            + '</a>'; nick = irclog.keys[0];
            irclog[ Msg[1] ] = "";
            }

        if(Msg[0] == "/part" and Object
        .keys(irclog).includes(Msg[1])) {
            document.getElementById
            (Msg[1]).remove();
            delete irclog[Msg[1]];
            }

        var data = {
         msg: Msg,
         nick: Nick
        };

        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/sendmsg/" + chan, true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(JSON.stringify(data));
    }

    # Must destroy irc bot once user leaves.
    window.onunload = function() {
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("GET", "/end/", false);
        xmlhttp.send();
    }

    function grablog() {
        for(k in irclog.keys())
        irclog[chan] += loadFile
        ("/chanlog/" + chan);

        document.getElementById("irclog")
        .innerHTML = irclog[chan];
    }

    function swtab(elem) {
        irclog[chan] += document
        .getElementById("irclog")
        .innerHTML;

        document.cookie = "chan=" + elem.name
        document.getElementById("irclog")
        .innerHTML = irclog[elem.name];
    }

    setInterval(grablog, 60000);
    </script><script type="text/python">
    def upload_complete(event):
        if event.target.status == 200:
            alert("File uploaded successfully!")

        else:
            alert("Upload failed!")

    def upload_data(data, fn):
        blob = window.Blob.new \
         ([data], {'type': 'text/plain'})  # Generic type data.
        file = window.File.new([blob], fn) # Send file as fn
        formdata = window.FormData.new()
        formdata.append("upload", file)
        req = window.XMLHttpRequest.new()
        req.open("POST", "/savefile", True)
        req.bind('load', upload_complete)
        req.send(formdata)

    def ide_run():
        exec(document \
         ['botcode'].value)

    def ide_load(sbox):
        if sbox.value == "new":
            bots['new'] = ''

        document['botcode'].value \
         = bots[sbox.value]
        curbot = sbox.value

    def ide_save():
        if curbot = "new":
            newname = prompt("Bot's name:")
            val = bots[sbox.value]
            del (bots[sbox.value])
            bots[newname] = document \
             ['botcode'].value

        else:
            bots[curbot] = \
             document['botcode'].value

    </script>"""

@route("/end/")
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
    dat = _bot[uuid].chanlog[chan]
    _bot[uuid].chanlog[chan] = ""
    return dat

@route("/sendmsg/<chan>")
def sendmsg(chan):
    uuid = request.cookies.get("uuid")
    msg = request.forms.get("msg")
    nick = request.forms.get("nick")
    chan = request.forms.get("chan")
    if msg.strip()[0] == "/":
        msg = msg.split(' ')
        if msg[0] == "/join":
            _bot[uuid].join(msg[1])
            return

        if msg[0] == "/part":
            _bot[uuid].part(msg[1])
            return

        if msg[0] == "/list":
            _bot[uuid].list()
            _bot[uuid].chanlog[chan] \
             += _bot [uuid].chans
            _bot[uuid].chans = ""
            return

        if msg[0] == "/send":
            _bot[uuid].send_file(msg[1], msg[2])

    _bot[uuid].connection.privmsg(chan, \
     "%s>> %s" % (nick, msg))

@route("/userfiles/<fname>")
def user_files(username, fname):
    uuid = request.cookies.get("uuid")
    file = request.files.get('upload')

    if not file:
        z = zipfile.ZipFile(uuid + ".zip", "r")
        return z.read(fname)

    else:
        z = zipfile.ZipFile(uuid + ".zip", "w")
        z.write(file.filename, file.file.read())
        z.close()

@route("/listfiles/")
def listfiles():
    c = request.cookies.get("uuid")
    z = zipfile.ZipFile(uuid + ".zip", "r")
    nl = z.namelist()

    for n in nl:
        html = '<a href="/userfiles/' \
         + n + '">' + n + '</a>'

    return html

def new_user():
    newuser = _user_prefix + str(_user_iter)
    _user_iter += 1
    return newuser

_servers = \
{"rizon": ("irc.rizon.org", 6667), \
"efnet": ("irc.prison.org", 6667)}

_user_iter = 0
_user_prefix = "dluser_"
_default_serv = _servers['rizon']
_default_chan = "dreadlink_technate"
run(host="localhost", port=8080)
