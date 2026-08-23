#! /usr/bin/env python
# (C) Paulus Madison Hay
# License: gplv3

import irc.bot
import irc.strings
from bot_boilerplate import boilerplate
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
from salmon.mail import MailResponse
from salmon.routing import route
from salmon.server import Relay
email_servr = 'ircmail.com'
mainclass = 'emailbot'
from hashlib import md5
from os import system
email_accts = {}
user_emails = {}

# Maybe this script might impersonate
# someone else's email over the internet.
# useful for phishing trojan attacks

email_servr = 'ircmail
helpmsg = """IRC email SVC v1.0
Commands available:

!join [username] [password]
Creates an account [username] with [password]
pasword to access and recieve emails later.

!login [username] [password]
Logs into your account [username] with password
[password] to use your account now.

---------------------
-- While logged in --
---------------------

!check-email
Lists your recieved emails and allows 
selection of an email for view.

!send-email [address]
Send an email to [adress].
"""

def update_emdb():
    emdb = json.loads(open( \
     'emails.json', 'r').read())
    # Remove deleted emails.
    for emaddr in emdb.keys( ):
        for em in range(len(emdb[emaddr])):
            if not emdb[emaddr][em] in \
             user_emails[emaddr]:
                del(emdb[emaddr][em])

    # Add new emails.
    for emaddr in user_emails.keys():
        for em in range(len(user_emails[emaddr])):
            if not user_emails[emaddr][em] in
             emdb[emaddr]: emdb[emaddr] += [em]

    y = open('emails.json', 'w')
    y.write(json.dumps(emdb))
    y.close()

def load_emdb():
    emdb = json.loads(open( \
     'emails.json', 'r'.read())
    user_emails = emdb

@route('(emailaddr)@(host)', \
 emailaddr='[a-z]+' \
 emailhost='[a-z]+')
def gotemail(message, emailaddr, emailhost):
    if emailaddr + '@' + host in emails.keys():
        user_emails['%s@%s'%(emailaddr, \
         emailhost)] += [message]
        update_emdb()

class emailbot(boilerplate):
    def startbot(self, opts):
        self.channel = opts['chan']
        self.server  = opts['serv']
        self.port    = opts['port']

        self.tmp_mesg = {}
        self.tmp_dest = {}
        self.tmp_user = {}
        self.tmp_iter = {}

        self.tmp_email_content = {}
        self.tmp_email_subject = {}
        self.tmp_emacct = {}

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_privmsg(self, c, e):
        cmd = e.arguments[0].split(' ')
        nick = e.source.nick

        if nick in multi.keys():
            if multi[nick] == "send_email_subject":
                self.multi[nick] = 'send_email_content'
                self.tmp_email_subject[nick] = ' '.join(cmd)
                c.privmsg(nick, "Type Email content ending with")
                c.privmsg(nick, 'the keyword "end" by itself.')
                self.temp_mesg = ''
                return

            # Note: User will create zombie
            # sessions if they leave - there
            # is no timeout.

            if self.multi[nick] == 'send_email_content':
                if cmd[0] == 'end':
                    r = Relay(host = None)
                    msg = self.tmp_mesg[nick]
                    c.privmsg("Sending email...")
                    message =  MailResponse( \
                     Body =    self.tmp_mesg[nick], \
                     To =      self.tmp_dest[nick], \
                     From =   self.email_ses[nick], \
                     Subject = self.tmp_email_subject[nick])

                    r.deliver(message)
                    del(self.tmp_email_subject[nick])
                    del(self.tmp_mesg[nick])
                    del(self.multi[nick])
                    return

                else: self.tmp_mesg \
                 [nick] += ' '.join(cmd)

            # Check for commands from user.
            if self.multi[nick] == 'select_email':
                user = self.user_ses[nick]
                email = user_emails [user]

                if self.tmp_iter[nick] < len(email) \
                 and cmd[0] == "more":
                    for i in range(10):
                        self.tmp_iter[nick] += 1
                        sub = email[self.tmp_iter[nick]]
                        c.privmsg (nick, "[%d] Subject: %s" \
                         % ( self.tmp_iter[nick], sub[0] ))
                        if self.tmp_iter[nick] ==len(email):
                            break

                # Option input
                elif cmd[0] == "sel":
                    del(self.multi[nick])
                    del(self.tmp_iter[nick])
                    ema = email[int(cmd[1])]
                    c.privmsg(nick, "Subject: " + ema[0])
                    c.privmsg(nick, "Content: ")
                    for ln in ema[1].split('\n'):
                        c.privmsg(nick, ln)

                elif cmd[0] == "del":
                    del(user_emails \
                     [user][int(cmd[1])])
                    del(self.tmp_iter[nick])
                    del(self.multi[nick])
                    update_emdb()

        if cmd[0] == '!join': # build addr.
            user = cmd[1] # Gather user and password
            pasw = cmd[2] # information.

            tmp_emacct = '%s@%s' \
             % (user, email_servr)

            # Reject username proposal.
            if tmp_emacct in self.email_accts.keys():
                c.privmsg(nick, "%s taken." % tmp_emacct)
                return

            self.email_accts[user] = {}
            paswd = hashlib.md5.new(pasw)
            paswd = paswd.hexdigest()
            self.email_accts[user] \
             ['passwd'] = passwd

        elif cmd[0] == '!login':
            if nick not in self.email_ses.keys():
                user, pasw = tuple(cmd[1:3])
                hash = hashlib.md5.new(pasw)
                hash = hash.hexdigest()

                if email_accts[user]['passwd'] == hash:
                    self.email_ses[nick] = user

        if nick in self.email_ses.keys():
            if cmd[0] == '!send-email':
                c.privmsg(nick, "Enter subject:")
                self.multi[nick] = "send_email_subject"
                self.temp_dest[nick] = cmd[1]
                return

            if cmd[0] == "!check-email":
                ema = "%s@%s" % (self.email_ses[nick], email_servr)
                self.multi[nick] = 'select_email'
                i = user_emails[ema]

                for em in range(10):
                    self.tmp_iter[nick] += 1
                    emm = (em, i[em].split('\n\n')[1])
                    c.privmsg(nick, '[%d] Subject: %s' %em)
                    if len(i) <= 10 and em == len(i): break

                # Display help message.
                c.privmsg(nick, 'Type "sel [email no.]" to select and read an')
                c.privmsg(nick, 'email, and: "del [email no.]" to select, and')
                c.privmsg(nick, "delete an email that's listed, or "more" for")
                c.privmsg(nick, "more emails to be listed.")
                return

             if cmd[0] == "!help":
                 for l in helpmsg.split('\n'):
                     c.privmsg(nick, l)

            if cmd[0] == "!logout":
                del(self.email_ses[nick])
