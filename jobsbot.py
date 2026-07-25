#! /usr/bin/env python
# (C) Paulus Madison Hay
# License: pending

# This bot is intended to ultimately
# sell any form of intuellectual work.
# Hirers create listings containing
# job specs and quality standards
# to prospective freelancers.

# Employers create an extra ai criteria
# to be inserted into the system string
# when testing and qualifying the worker's
# code. The code is allowed to be sold
# once the ai qualifies it.

# Then a "salesman" ai program allows
# the customer to ask questions about
# the code and fully accept it b4
# buying it.

# This program should hide the code
# itself from the customer so that
# any looking at it is not free.

# Then if the customer accepts this
# code's dynamic AI description, he
# may be shown/given the latest code
# and the money escrow goes to
# the employee.

# Then if the customer is still
# unsatisfied with the code, he
# may continue discussing more
# iterations of the code for
# another money committment.

import ollama
import irc.bot
import irc.strings
from irc.client import \
 ip_numstr_to_quad, \
 ip_quad_to_numstr

from pydantic import BaseModel
from bot_boilerplate import boilerplate
from os import system
mainclass = "jobsbot"

import ollama

model_name = 'opencoder:1.5b'
# Initialize conversation with a system 
# prompt (optional) and a user message

empjudge = '''You angrily judge software
code for its structure, future-proof design,
bug-free ness, adherence to coding standards,
security flaws, and conformity to the
customer's request.

Your job is to proof read employee code
before it can be allowed to be sold. You are
the bullwhark between crapola and good writing.
You do not tolerate crap code written by luser
wannabe hackers especially. You have our company
standards to uphold!

Our standards: We buy and sell the best code
from and to the best coders. Accept no substitutes!
Suck code is unacceptable! Suck coders are
unacceptable. All code submitted must have
every block of code commented well and
descriptively, or you will report your
disgust of that code and its poor comments.
Any fever dream code shall be reported for
its insanity, conceptualism, and poor
logic. Any code with security flaws
must be reported.

You will provide a detailed [summary]
of the code explaining exactly how the
code works.

You will provide a detailed [report] of the code
provided according to this contract's premise. give
a stars [rating] from zero meaning your worst judgement,
to ten, your best judgement, and decision whether this
code is worthy of selling.

Code that is worthy of selling must be
rated at least seven stars and conform
perfectly to the customer's code
request.

If this code is sub-par, you will
report your disgust of it and its
writer to the customer.

content is the employee's
code to be judged.
'''

hirejudge = '''Programmers create the
best code when directed with simple
instructions. Your job is to qualify
thosse instructions.

The job must comply
with this standard:

* If the [feasibility_rating] is
  high, the clarity is good, and
  [simplicity] is high then the
  work is acceptable, and so
  [accepted] flag is True.

* You must estimate the difficulty level
  of the job to complete into [difficulty]
  Difficulty scale in order from lowest to
  highest: LO, L1, L2, MID, H3, H4, HI

* You must give a report on the feasibility
  that the job is completable at all into
  [feasibility-report] and a [feasibility_rating]
  from 0 to 100. 0 is an impossible paradox,
  and 100 is completely possible.

* You must report a var indicating
  the understandability of the job
  instructions called [simplicity]
  from 0 to 10. 0 is gibberish
  and 0 is elegant simplicity.

* You must estimate the overall
  clarity and understandability
  of the job description into
  [clarity]

* You must estimate the
  complexity of the job in
  practise and describe it
  into [complexity]

* The job must contain a
  readable description of the
  application the customer
  wants written for them.

* The job must specify the
  [programming_language]
  they want used, or its
  unspec and an application
  in any language may be
  responded.'''

class jobjudgeresp(BaseModel):
    complexity: str
    clarity:    str
    difficulty: str
    jdpass:     bool

class workjudgeresp(BaseModel):
    programming_language: str
    report:  str
    rating:  int
    summary: str

class jobsbot(boilerplate):
    def bot_init(self, opts):
        nick, server, port = opts['nick'], opts['server'], opts['port']
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nick, nick)
        irc.client.ServerConnection.buffer_class.encoding = "latin-1"
        self.cache = './cache.zip'
        self.channel = channel
        self.server = server
        self.hicost = 1 #BTC
        self.port = port

    # List results.
    def on_list(self, c, e):
        print(e.arguments)

    # When list finishes.
    def on_listend(self, c, e):
        print("on_listend triggered.")

    # when list starts.
    def on_liststart(self, c, e):
        print("on_liststart triggered.")

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def bot_welcome(self, c, e):
        #print(dir(irc.client))
        c.list()
        system('aplay beep.wav')
        print("Channel list over?")
        c.join(self.channel)
        c.join("#4taba")

    def gen_tmpfn(self):
        zf = zipfile.ZipFile(self.cache, 'r')
        l = zf .listfiles ( )
        if len(l) == 0: n = 0
        else: #find next tmp file
            n = int(sorted(l)[-1] \
             .split('.')[-2])
            n += 1

        return 'tmp.' + n

    def savedb(self):
        with zipfile.ZipFile(cache, 'w') as zf:
            zf.writestr(json.dumps({'jobs': \
             self.jobs,  'work': self.work, \
             'passwd':   self.passwd}))     \

    def on_privmsg(self, c, e):
        cmd = e.arguments[0].split(' ')
        nick = e.source.nick

        # TODONE:
        # Warning! Zsend_file requires temp
        # work files to be packed into a zipfile. 
        # Must create this feature.

        # Proposal:
        # a json file inside of a central
        # zipfile of anonymous temp files
        # organizing them.

        if nick in self.skillstest.keys():
            if qz == 30: pass
            else: ans = e.arguments[0]
            if qz[nick] > 0:
                testprg = '''Give the user a holistic programming
                 skills and aptitude test for the {prg} programming
                 language.'''.replace(' ' * 8, '')

                lang = self .testlang [nick]
                tfmt = tfmt .format(prg=lang)
                self.qz[nick] = 30

                tfmt = testprg.format()
                jobs = [{ 'role': 'system',  'content': tfmt}, \
                 {'role': 'user', 'content': 'Give a test question.'}]

                out = ollama.chat(         \
                 model='qwen2.5-coder:3b', \
                 messages = codejobs)

                c.privmsg (nick, out.content)
                self.testlastq[nick] = out.content

            else:
                prg = '''Respond with [pass] indicating
                 whether the question in the following
                 paragraph was answered correctly, and
                 [explanation] containing how the
                 question was correct or incorrect.'''

                class fmt(BaseModel):
                    explanation: str
                    pass: bool

                ans  = e.arguments[0]
                conv = [{'role': 'system', 'content': prg}
                        {'role': 'user',   'content': ans}

                prg += '\n\n'
                prg += self.lastq[nick]
                out  = ollama.chat(                 \
                 model  = 'qwen2.5-coder:3b',       \
                 format = fmt.model_json_schema(),  \
                 messages = conv)

                c.privmsg(nick, out.explanation)
                if not out.pass: self.testpass \
                 [nick] += [out.pass]

        if nick in self.mj_multi.keys():
            escrow = self.mj_multi[nick].escrow
            esret  = self.mj_multi[nick].employee-esret
            self.Zsend_file (self.mj_multi[nick].work, nick)
            system('electrum payto %s %d' % (esret, escrow))
            jnr = self.mj_multi[nick].jobnr
            for i in range(len(self.jobs)):
                if self.jobs[i].jobnr == jnr:
                    del(self.jobs[i])

            for i in range(len(self.work)):
                if self.work[i].jobnr == jnr:
                    del(self.work[i])

        if self.aj_multiline[e.source.nick]:
            self.tjob[e.source.nick] += e.arguments[0]
            if e.arguments[0] == "--":
                self.multiline[e.source.nick] = False
                self.employercoach (e.source.nick,  \
                 self.tbtcretaddr  [e.source.nick], \
                 self.tjob         [e.source.nick])

                del   (self.multiline[e.source.nick])
                del (self.tbtcretaddr[e.source.nick])
                del        (self.tjob[e.source.nick])

        if cmd[0] == '!skillstest':
            user_esret = cmd[1]
            self.usertest[nick] = cmd[1]
            self.qz[nick]

            testprg = '''Give the user a holistic programming
             skills and aptitude test for the {prg} programming
             language.'''.replace(' ' * 8, '')  

            lang = self .testlang [nick]
            tfmt = tfmt .format(prg=lang)

            tfmt = testprg.format()
            self.usertest[nick] = [] #Persistent variable.
            self.testfmt = [{ 'role': 'system', 'content': tfmt}, \
             {'role': 'user', 'content': 'Give a test question.'}]

            for i in range(30):
                out = ollama.chat(         \
                 model='qwen2.5-coder:3b', \
                 messages = codejobs)

                # Persistent variable.
                self.usertest[nick] += [out.content]

            for prg in prgz:
                tfmt = testprg.format()
                jobs = [{'role': 'system', 'content': tfmt}, \
                 {'role': 'system', 'content': \
                  'Give a test question.'}]

                 out = ollama.chat(         \
                  model='qwen2.5-coder:3b', \
                  format=workjudgeresp      \
                  .model_json_schema(),     \
                  messages = codejobs)

                 out.'''

        if cmd [0] == '!myjobs':
            if cmd[1] == 'list':
                for i in range(len(self.work)):
                    if self.work[i].['employer-esret'] != esret: continue
                    c.privmsg(nick, self.work[i] .job)
                    c.privmsg(nick, "....")

            else:
                esret, tmenu = cmd[1], []
                passw = cmd[2] # Password check
                if passw != self.passwd[esret]: return
                for i in range(len(self.work)):
                    if self.work[i].['employer-esret'] != esret: continue
                    tmenu += [{'line': i, 'work': self.work [i]]

                work = self.work[tmenu \
                 [int(e.arguments[0])].line]
                tmpjudge = empjudge + '\n\n'
                tmpjudge += '''You are judging the employee's
                submitted work for the hirer. Hide the code
                from the user, and paraphrase any necessary
                code snippets in your [review].'''

                codejobs = [ \
                 {"role": "system",  "content":  tmpjudge}, \
                 {'role': 'system',  'content':  work.job}, \
                 {'role':   'user',  'content': work.work}]

                out = ollama.chat(         \
                 model='qwen2.5-coder:3b', \
                 format=workjudgeresp      \
                 .model_json_schema(),     \
                 messages = codejobs)

                c.privmsg(nick, out .report)
                c.privmsg(nick, '%s/10 stars.' \
                 % out.rating) # Show rating.
                self .mj_multi [nick] = work

        if cmd[0] == '!addjob':
            self.tbtcretaddr [e.source.nick] = cmd[1]
            self.tjob[e.source.nick] = e.arguments[0]
            self .aj_multiline [e.source.nick] = True
            return

        if cmd[0] == '!getjobs':
            certs = testuser(nick)
            # testuser is imaginary. Later it will
            # dynamically generate programming tests
            # for each programming language.

            if cmd[1] == 'list':
                for j in self.jobs:
                    c.privmsg(e.source.nick, 'option %d' % II
                    c.privmsg(e.source.nick,      j.job)
                    c.privmsg(e.source.nick,   j.escrow)

                return

            else: #Select and load job
                jobsel = int(self.jobs [e.arguments[0])
                esret  = self.tseljob  [e.source.nick]
                jobsel = self.jobs     [e.arguments[0]]

                c.privmsg         (nick, "Job description")
                c.privmsg       (e.source.nick, jobsel.job)
                c.privmsg             (nick, "Job salary:")
                c.privmsg    (e.source.nick, jobsel.escrow)
                c.privmsg   (nick, "Please upload work...")
                while e.source.nick not in self.rdcc.keys():
                    pass # Wait for a download

                c.privmsg("Downloading work...")
                while e.source.nick in self.rdcc.keys():
                    pass # Wait until download finished.

                work = self.tmp_lastfile[e.source.nick]
                del(self.lastfile[e.source.nick])

                codejobs = \
                 [{"role": "system", "content":   empjudge},
                 {'role':  'system', 'content': jobsel.job},
                 {'role':  'user',   'content':       work}]

                out = ollama.chat
                 (model='qwen2.5-coder:3b',
                 format=jobjudgeresp.model_json_schema(),
                 messages=reqjudge)

                c.privmsg (e.source.nick, out.review)
                workfmt = workfmt.replace(' '*12, '')
                if(out.rating > 5):
                    self.work [jobsel.esret] += \
                     [{'work': work,  'job':    jobsel.job, 'employer-esret':  \
                     jobsel.esret, 'escrow': jobsel.escrow, 'employee-esret':  \
                     esret}] # update db
                    self.savedb()

                else: # Reject employee work
                    c.privmsg(e.source.nick, "This work is unacceptable!")
                    c.privmsg(e.source.nick, out.review)
                    return

    def employercoach(nick, tba, jd):
        reqjudge = \
            [{'role': 'system', 'content': hirejudge},
             {'user': "system", 'content': jd}]

        out = ollama.chat \
         (model    = 'qwen2.5-coder:3b',
          format   = jobjudgeresp.model_json_schema(),
          messages = reqjudge)

        c = c.connection
        c.privmsg(nick, out.complexity)
        c.privmsg(nick, out.difficulty)
        c.privmsg(nick, out.clarity)

        if out.jdpass:
            c.privmsg(nick, \
             "Congratulations! Your job " \
             + "description is accepted." \
             + "Please deposit escrow...")

            cost = self.hicost * (0.01 * out.costperc)
            chaching = checkout(nick, cost +self.cost)
            if not chaching:
                c.privmsg(nick, \
                 "Could not verify transaction.")
                return

            # Find latest job number.
            jnrz = [i.jobnr for i in self.jobs.keys()]
            jnr = max(jnrz) + 1

            tj = gentmpfn()
            with zipfile.ZipFile(self.cache, 'w') as tjj:
                tjj.writestr(tj, jd)

            self.jobs += [{  \
             'escrow': cost, \
             'esret':  tba,  \
             'jobnr':  jnr,  \
             'job':    tj}]
             self .savedb()

        else:
            c.privmsg(nick, "Your job" \
             + "description is unacceptable."

    def on_pubmsg(self, c, e):
        print("e.source:")
        print(e.target)

        a = e.arguments[0].split(":", 1)
        if len(a) > 1 and irc.strings.lower(a[0]) \
         == irc.strings.lower(self.connection.get_nickname()):
            self.do_command(e, a[1].strip())

        return

    def Zsend_file(self, filename, reciever):
        self.dcc += [self.dcc_listen("raw")]
        f = ZipFile.open(self.cache + '.zip', 'rb')

        for x in f.infolist():
            if filename == x.filename:
                break

            fsize = x.file_size

        msg_parts = map(
            str,
            (
                'SEND',
                os.path.basename(filename),
                irc.client.ip_quad_to_numstr \
                 (self.dcc[-1].localaddress),
                self.dcc[-1].localport,
                fsize,
            ),
        )

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
                c.privmsg(rnick, "Recieved " + self.filename)
                self.tmp_lastfile[rnick] = dstream[rnick]
                # Create a temporary variable
                # containing the last file
                # [rnick] downloaded.

                # Finished recieving
                del(self.filename    [rnick])
                del(self.dstream     [rnick])
                del(self.rfsize      [rnick])
                del(self.rdcc        [rnick])
                return

            self.dstream[rnick] += data
            self.rdcc[rnick].send_bytes \
             (struct.pack("!I", data))

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
