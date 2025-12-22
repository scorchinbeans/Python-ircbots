
# (C) Paulus Madison Hay
# License: GPLV2

from bot_boilerplate import boilerplate
from os import system, popen
from schedule import repeat
from schedule import every
import json, time, random
mainclass = 'blackjackbot'
import irc.bot
_isweb = {}

class blackjack_cli:
    def __init__(self):
        self.deck, self.status = [], {}
        suits = ["clubs", "diamonds", "hearts", "spades"]
        self.deck += ["J diamonds", "Q diamonds", "K diamonds"]
        self.deck += ["J hearts", "Q hearts", "K hearts"]
        self.deck += ["J spades", "Q spades", "K spades"]
        self.deck += ["J clubs", "Q clubs", "K clubs"]
        every(3).seconds.do(self.timetick)
        self.status['profit'] = 0

        for suit in suits:
            for nr in range(10):
                card = str(nr) + " " + suit
                self.deck += [card]

        self.shuffle()
        self.turntimer = 0
        self.winner = None
        self.players = []
        self.ante = False
        self.antebet = 0
        self.stayed = []
        self.folded = []
        self.addrs = {}
        self.bets = {}
        self.pot = 0

    def tohtml(self, h):
       hand = self.hands[h]
       rstr = ''

       for i in hand:
           num = i.split(' ')
           suit = num[1]
           num = num[0]
           uni = {'spades': "1f0a1", \
            'hearts': '1f0b1', \
            'diamonds': '1f0c1', \
            'clubs': '1f0d1'}

           x = int(uni[suit], 16)
           rstr += ["$#x" + hex(x+num)]

       return rstr

    def add_debts(self, user, debt):
        system('echo "%s::%s\n" >> debtledger.txt' % (user, debt))

    def newgame(self):
        self.deal()

        # Init self.bets.
        for p in self.players:
            self.addrs[p] = ''
            self.bets[p] = 0

        c = self.conn
        self.turn = self.players[0]
        self.nextturn()

    def endgame(self):
        maxhand = 0
        for k, v in self.hands.items():
            if self.calchand(v) > maxhand:
                maxhand = self.calchand(v)
                maxuser = k

        c = self.conn
        self.winner = maxuser
        charge = self.pot * 0.15
        tmp0 = self.addrs[self.winner]
        tmp1 = self.pot - charge

        if tmp1 > 0:
            system("electrum sendto %s %f" \
             % (tmp0, tmp1))

        for p in self.players:
            c.privmsg(p, "This game is over.")
            c.privmsg(p, self.winner +" wins")

        self.status['profit'] += charge
        c.privmsg(self.winner, "Sent you your bitcoins.")
        c.privmsg(self.winner, "Won %d." % tmp1)

        self.pot = 0
        self.addrs = []
        self.players = []
        self.ingame = False
        self.tout = {}
        self.die(self)

    def calchand(self, hand):
        vals = {"0":0,"1":1,"2":2,"3":3, \
            "4":4,"5":5,"6":6,"7":7,"8":8, \
            "9":9,"10":10,"A":1,"J":11, \
            "Q":12,"K":13}

        handval = 0
        for card in hand:
            val = card.split(" ")
            val = vals[val[0]]
            handval += val

        return handval

    def shuffle(self):
        deck = self.deck
        deck2 = []

        while deck:
            n = random.randint(0, len(deck)-1)
            deck2 += [deck.pop(n)]

        self.deck = deck2

    def deal(self):
        self.hands = {}
        for p in self.players:
            self.hands[p] = []
            for i in range(2):
                self.hands[p] += \
                 [self.deck.pop()]

    def hit(self, player):
        self.hands[player] += [self.deck.pop()]
        if(self.calchand(self.hands[player]) > 21):
            self.folded += [player]

    def stay(self, player):
        self.stayed += [player]

    def fold(self, player):
        self.folded += [player]

    def turnend(self):
        c, sw = self.conn, True
        c.privmsg(self.turn, "Turn ended.")
        if (len(self.stayed) + len(self.folded)) \
         == len(self.players) - 1 and self.turn \
         not in (self.stayed + self.folded):
            c.privmsg(self.turn, \
             "Other players are finished.")

        if len(self.stayed) \
         + len(self.folded) \
         == len(self.players):
            self.endgame()
            return

        while (self.turn in self.stayed \
         or self.turn in self.folded) or sw:
            nturn = self.players.index(self.turn)
            nturn = (nturn + 1) % len(self.players)
            self.turn = self.players[nturn]
            print("Turned " + self.turn)
            if sw: sw = False

        self.nextturn()

    def nextturn(self):
        self.turntimer = time.time()
        c = self.conn # Get connection
        c.privmsg(self.turn, "blackjackbot v1.0")
        c.privmsg(self.turn, "30 secs b4 turn end.")
        c.privmsg(self.turn, "It's your turn.")

        if self.ante:
            c.privmsg(self.turn, " ")
            c.privmsg(self.turn, "Another player has called ante up.")
            c.privmsg(self.turn, "You must bet as much as he he has ")
            c.privmsg(self.turn, "or fold. Ante to: %d" %self.antebet)

        b = ','.join(map(str, self.bets.values()))
        c.privmsg(self.turn, "Current bets: " + b)
        c.privmsg(self.turn, "Your bet: %d" % self.bets[self.turn])
        c.privmsg(self.turn, "Your hand:")
        if not _isweb[self.turn]:
            shand = self.hands[self.turn]
        else: shand = self.tohtml(self.turn)
        for card in shand:
            c.privmsg(self.turn, card)

    def command(self, cmd, user):
        cmd = cmd.split(' ')
        c = self.conn # Connection
        if self.ante: # Make players ante
            for i in self.bets.values( ):
                if i >= self.antebet:
                    antes += 1

            if antes == len(game.bets):
                self.antebet = 0
                self.ante = False

            if self.bets[nick] < self.antebet \
             and cmd[0] not in ["!bet", "!fold"]:
                self.turnend()
                return

        if cmd[0] == "!help":
            c.privmsg(user, "notes:")
            c.privmsg(user, "* Your turn will time out and")
            c.privmsg(user, "skip to the next player 3 times")
            c.privmsg(user, "before it forces you to fold")
            c.privmsg(user, "This is to prevent people leaving")
            c.privmsg(user, "in midgame from freezing the game.")
            c.privmsg(user, "* its %s's turn. " % self.turn)
            c.privmsg(user, " ")
            c.privmsg(user, "Commands:")
            c.privmsg(user, "!setaddr [your adress]")
            c.privmsg(user, "Set adress to send your winnings to.")
            c.privmsg(user, " ")
            c.privmsg(user, "!bet")
            c.privmsg(user, "Bet bitcoins on this game.")
            c.privmsg(user, " ")
            c.privmsg(user, "!anteup")
            c.privmsg(user, "If you have bet the most, will")
            c.privmsg(user, "Force other players to bet as")
            c.privmsg(user, "much as you have, or leave.")
            c.privmsg(user, " ")
            c.privmsg(user, "!hit")
            c.privmsg(user, "Draw a card.")
            c.privmsg(user, " ")
            c.privmsg(user, "!stay")
            c.privmsg(user, "Submit your hand")
            c.privmsg(user, " ")
            c.privmsg(user, "!fold")
            c.privmsg(user, "Quit game and automatically lose.")

        if cmd[0] == "!hit" \
         and user == self.turn:
            self.hit(user)
            c.privmsg(user, "Hit 1 card!")
            self.turnend()

        elif cmd[0] == "!stay" \
         and user == self.turn:
            self.stay(user)
            self.turnend()

        if cmd[0] == '!fold' \
         and user == self.turn:
            self.fold(user)
            self.turnend()

        elif self.bets[user] == \
         max(self.bets.values()) \
         and (cmd == "!anteup") \
         and user == self.turn:
            self.antebet = self.bets[user]
            self.ante = True
            self.turnend()
            return

        elif cmd[0] == "!set-addr" \
         and user == self.turn:
            self.addrs[user] = cmd[1]

        elif cmd[0] == "!bet" \
         and user == self.turn:
            c = self.conn # Set connection
            if not self.addrs[user]:
               c.privmsg(user, """Have not
                set adress yet! Use: !setaddr
                [reciept addr]""")
               return

            ep = popen("electrum \
             add_request " + cmd[1], "r")
            reqjson = json.loads(ep.read())
            rid = reqjson["request_id"]
            htm = reqjson["URI"]
            bet = int(cmd[1])
            rstr = ""

            c.privmsg(user, "Send bitcoins here.")
            c.privmsg(user, "You have 30 seconds")
            c.privmsg(user, "before timeout or you")
            c.privmsg(user, "will go this far into")
            c.privmsg(user, "debt.")
            c.privmsg(user, htm)

            bc = time.time() + 30
            while rstr != "Completed" and time.time() <= bc:
                ep = popen("electrum get_request " + rid, "r")
                rstr = json.loads(ep.read())["status_str"]
                ep.close()

            if rstr != "Completed":
                c.privmsg(user, "Transaction not completed")
                c.privmsg(user, "Loaning the user his bet.")
                if sum(self.debts. \
                 values) < self.debtlimit:
                    self.debts[rnick] += bet

                else:
                    c.privmsg(user, "Reached loan limit.")
                    c.privmsg(user, "Cancelling ur loan.")
                    bet = 0

            self.pot += bet
            self.bets[user] += bet
            c.privmsg(user, "Transaction completed.")
            c.privmsg(user, "Bet %d bitcoins." % bet)
            if self.ante: # End turn at bet if ante.
                self.turnend()
                return

    def timetick(self):
        c = self.conn # Set connection
        if time.time() >= (self.turntimer \
         + 30) and self.ingame == True:
            self.fold(self.turn)
            self.turnend()

        return

class blackjackbot(boilerplate):
    def bot_init(self, opts):
        self.status = {} # Self status
        self.status['started'] = False

        self.chans = []
        self.games = []
        self.nick = opts['nick']
        self.status['gamesplayed'] = 0
        self.status['chans'] = []
        self.status['profit'] = 0
        self.lastturntimer = None
        self.Terminate = False
        self.completed = False
        self.gamesplayed = 0
        self.ingame = False
        self.players = []
        self.game  = None
        self.profit = 0
        self.addrs = {}
        self.tout = {}
        self.bets = {}
        self.nmsg = 0
        self.pot  = 0

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def bot_welcome(self, c, e):
        self.status['started'] = True
        print("Started bot.")

    def on_ctcp(self, c, e):
        nick = e.source.nick
        if event.arguments[0] == "VERSION":
            _isweb[nick] = False # Initialize nick ver.
            if e.arguments[1].split(' ')[0] == "webirc":
                _isweb[nick] = True # Is webirc client.

            elif e.arguments[1].split(' ')[0] == 'searchbot':
                c.send_ctcp(nick, 'VERSION', 'blackjackbot v1.0 -- \
                 A fun bitcoin blackjack gambling service.')

    def on_privmsg(self, c, e):
        cmd = e.arguments[0]
        nick = e.source.nick
        scmd = cmd.split(' ')
        chan = e.target
        ingame = False
        game = None

        if nick not in _isweb.keys():
            self.send_ctcp(nick, "VERSION", "blackjackbot v1.0")

        for i in range(len(self.games)):
            if nick in self.games[i].players:
                game = self.games[i]
                ingame = True
                break

        if ingame: game.command(cmd, nick)
        if cmd == "!join" and not ingame:
            print("User %s joined a game!" % nick)
            c.privmsg(nick, "Joined game.")

            self.players += [nick]
            if len(self.players) == 1:
                self.games += [blackjack()]

            if len(self.players) == 2:
                print("Starting game...")
                self.games[-1].conn = self.connection
                self.games[-1].players = self.players
                self.games[-1].turn = self.players[0]
                self.games[-1].die = self.gamedie
                self.games[-1].ingame = True
                self.games[-1].newgame()
                self.players = []

        elif cmd == "!help" and not ingame:
            c.privmsg(nick, "(C) gplv2 Blackjackbot") # gplv2 2.c
            c.privmsg(nick, "!join: Join the next game when started.")
            c.privmsg(nick, "You will be PM'd when the game starts.")

    def gamedie(self, gameclass):
        for i in range(len(self.games)):
            if gameclass == self.games[i]:
                game = self.games[i]
                break

        profit = game.status['profit']
        self.status['profit'] = profit
        self.status['gamesplayed'] +=1
        del(self.games[i])

    def on_kick(self, c, e):
        self.connection.join(e.target)

    def cmd_parser(self, cmd):
        cmd = cmd.split(' ')
        if cmd[0] == "help":
            print("join [channel]: Join channel.")

        elif cmd[0] == "games":
            print("List the stats of games past.")

        elif cmd[0] == "games":
            for i in self.games:
                print(i.players)
