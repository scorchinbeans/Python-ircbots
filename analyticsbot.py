from bot_boilerplate import boilerplate
from threading import Thread
mainclass = 'analyticsbot'
import irc

class analyticsbot(boilerplate):
    def bot_init(self, opts):
        irc.client.ServerConnection.buffer_class.errors = "replace"
        print("Statbot waiting for server welcome.")
        self.ajbots = opts['botifs']
        self.donelisting = False
        self.trafrank = []
        self.userrank = []
        self.complete = 0
        self.traffic = {}
        self.tcont = cont

    def bot_welcome(self, c, e):
        # time.sleep(30)
        print("Server welcomed statbot.")
        print("Starting to stat server...")
        c.list() # List the channels.

    def on_join(self, c, e):
        self.joined = self.joined + 1
        tmp = (self.joined, len(self.chans), e.target)
        print("Joined: (%d/%d) %s" % tmp)
        self.traffic[e.target] = 0
        # time.sleep(3)

        if self.joined == len(self.chans):
            if self.tcont: # Restart bot.
                self.rankchans()
                self.roundsdone += 1
                self.resetflag = True
                for ch in self.channels.keys():
                    c.part(ch) # Part from any
                               # joined channels.

                # Prevent it from joining
                return # another channel.

            else: # Kill bot.
                self.rankchans()
                self.complete += True
                if not self.cont: self.die() # Run once.
                for c in self.channels.items(): c.part(c[0])
                self.autojoin()
                sleep(60 * 4)
                c.list()

        # Join a channel or process and reset.
        if self.joined % self.itr == 0: # multiple of itr?
            self.rankchans()  # Process the channel stats.
            for chi in self.channels.keys():
                c.part(chi) # Part from any
                            # joined chans.

        # If joined is not a multiple of itr.
        else: c.join(self.chans[self.joined])

    def on_part(self, c, e):
        del(self.chans[e.target])
        self.parted += 1 # Iterate.
        if len(self.channels.keys()) == 0:
            if self.resetflag: c.list()
            else: c.join(self.chans[self.joined])

    def on_list(self, c, e):
        self.chans += [e.arguments[0]]
        print(e.arguments[0])
        self.complete = False

    def on_liststart(self, c, e):
        print("Getting channel list.")
        self.fintrafrank = self.trafrank
        self.finuserrank = self.userrank
        self.resetflag = False
        self.trafstats = {}
        self.userstats = {}
        self.trafrank = []
        self.userrank = []
        self.chans = []
        self.joined = 0
        self.parted = 0
        beep()

    def on_listend(self, c, e):
        print("Channel listing done.")
        beep() # Audible demarking bell
        time.sleep(5) # Wait 5s.
        c.join(self.chans[0])

    def rankchans(self):
        chp = [] # Rank channels/stats
        print("Ranking channels by nr. of users.")
        for chname, chobj in self.channels.items():
            self.userstats[chname] = len(chobj.users())
            print("Channel name: %s\nUsers count: %d" \
             % (chname, self.userstats[chname]))
            chp += [chname]

        ts = 15 # unit: #pubmsgs/ts secs
        self.traffic = {} # reset traffic
        for t in chp: self.traffic[t] = 0
        print("Scanning traffic: [", end="")
        for i in range(15): # trafstats
            print("#", end="")
            stdout.flush()
            time.sleep( 1)

        print("] Done.\n")
        tmark = self.traffic
        for i in chp: self.trafstats[i] = tmark[i]
        self.trafrank = self.ranksort(self.trafstats)
        self.userrank = self.ranksort(self.userstats)

    def ranksort(self, stats):
        rank = [list(stats.keys())[0]]
        for i in list(stats.keys()):
            ta = stats[rank[0]]
            tb = stats[rank[-1]]
            if stats[i] > tb: rank += [i]
            elif stats[i] < ta: rank = [i] + rank
            else: # stats -> rank-sorted channels
                for j in range(len(rank)-1):
                    schan = stats[rank[j]]
                    nchan = stats[rank[j+1]]
                    if stats[i] > schan and \
                     stats[i] < nchan:
                        rank = rank[:j] + [i] + rank[j+1:]
                        break

        return rank

    def poprank(self):
        ur = self.userrank
        tr = self.trafrank
        pr = [] # Popularity rating.
        # Indicates list of highest
        # ranking channels by both
        # user numbers ranking and
        # traffic activity ranking.

        while tr:
            for x in tr:
                y = ur.find(x)
                if y + x > maxno:
                    maxno = y + x
                    maxc = x

            pr += [tr.pop(maxc)]

        return pr

    def on_pubmsg(self, c, e):
        if e.target in self.traffic.keys():
            self.traffic[e.target] += 1

    def cmd_parser(self, command):
        cmd = command.split(' ')
        if cmd[0] == "popjoin":
            serv = cmd[1]
            for c in self.poprank():
                self.ajbots[serv].join(c)

        elif cmd[0] == "stats":
            print("Users ranking:")
            print('\n'.join(self.userrank))
            print("\nTraffic ranking:")
            print('\n'.join(self.trafrank))
            print("\nUsers/traffic ranking:")
            print('\n'.join(self.poprank()))

# using statbot, you can find all of
# the most popular channels in real
# time, on which to conduct the most
# business. Much more powerful than
# a website, which is only in one
# place.
