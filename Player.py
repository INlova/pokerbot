import itertools
from Deck import Deck

"""
Player bot
"""
class Player:
    def unpack(self, word, packet):
        if word=="NEWGAME":
            self.name, self.opp1name, self.opp2name = packet.pop(0), packet.pop(0), packet.pop(0)
            self.stacksize, self.bb, self.numhands, self.timebank = int(packet.pop(0)), int(packet.pop(0)), int(packet.pop(0)), float(packet.pop(0))
        elif word=="NEWHAND":
            self.handid, self.seat = int(packet.pop(0)), int(packet.pop(0))
            self.holecards = packet.pop(0), packet.pop(0)
            self.stacksizes = {1: int(packet.pop(0)), 2: int(packet.pop(0)), 3: int(packet.pop(0))}
            self.playernames = {'button': packet.pop(0), 'sb': packet.pop(0), 'bb': packet.pop(0)}
            self.numactiveplayers = int(packet.pop(0))
            self.activeplayers = {'button': bool(packet.pop(0)), 'sb': bool(packet.pop(0)), 'bb': bool(packet.pop(0))}
            self.timebank = float(packet.pop(0))
            self.raisecount = 0
            self.street = "PRE-FLOP"
        elif word=="GETACTION":
            self.potsize = int(packet.pop(0))
            self.numboardcards = int(packet.pop(0))
            self.boardcards = []
            for i in range(self.numboardcards):
                self.boardcards.append(packet.pop(0))
            self.stacksizes[1], self.stacksizes[2], self.stacksizes[3] = int(packet.pop(0)), int(packet.pop(0)), int(packet.pop(0))
            self.numactiveplayers = int(packet.pop(0))
            self.activeplayers['button'], self.activeplayers['sb'], self.activeplayers['bb'] = bool(packet.pop(0)), bool(packet.pop(0)), bool(packet.pop(0))
            self.numlastactions = int(packet.pop(0))
            self.lastactions = {}
            self.legalactions = {}
            for i in range(self.numlastactions):
                perfaction = packet.pop(0).split(":")
                action = perfaction.pop(0)
                if action != "DEAL":
                    actor = perfaction.pop()
                    self.lastactions[actor] = action
                    if action == "RAISE":
                        self.raisecount += 1
                else:
                    board = perfaction.pop()
                    if self.street != board:
                        self.raisecount = 0
                    self.street = board
            self.numlegalactions = int(packet.pop(0))
            for i in range(self.numlegalactions):
                action = packet.pop(0).split(":",1)
                if len(action) == 1:
                    self.legalactions[action.pop()] = True
                else:
                    self.legalactions[action.pop(0)] = action.pop().split(":")
            self.timebank = packet.pop(0)
        elif word=="HANDOVER":
            self.stacksizes[1], self.stacksizes[2], self.stacksizes[3] = int(packet.pop(0)), int(packet.pop(0)), int(packet.pop(0))
            self.numboardcards = int(packet.pop(0))
            self.boardcards = []
            for i in range(self.numboardcards):
                self.boardcards.append(packet.pop(0))
            self.numlastactions = int(packet.pop(0))
            for i in range(self.numlastactions):
                perfaction = packet.pop(0).split(":")
                action = perfaction.pop(0)
                actor = perfaction.pop()
                self.lastactions[actor] = action
            self.timebank = packet.pop(0)
    def ispreflop(self):
        return self.street == "PRE-FLOP"
    def isflop(self):
        return self.street == "FLOP"
    def isturn(self):
        return self.street == "TURN"
    def isriver(self):
        return self.street == "RIVER"
    def preflop(self, input_socket, d):
        if d.istophand(self.holecards):
            if 'BET' in self.legalactions:
                input_socket.send("BET:"+self.legalactions['BET'][1]+"\n")
            elif 'RAISE' in self.legalactions and self.raisecount < 2:
                input_socket.send("RAISE:"+self.legalactions['RAISE'][1]+"\n")
            elif 'CALL' in self.legalactions:
                input_socket.send("CALL:"+self.legalactions['CALL'][0]+"\n")
        elif d.ismedhand(self.holecards):
            if 'BET' in self.legalactions:
                input_socket.send("BET:"+self.legalactions['BET'][1]+"\n")
            elif 'RAISE' in self.legalactions and self.raisecount < 2:
                input_socket.send("RAISE:"+self.legalactions['RAISE'][1]+"\n")
            elif 'CALL' in self.legalactions and self.raisecount < 3:
                input_socket.send("CALL:"+self.legalactions['CALL'][0]+"\n")
            else:
                input_socket.send("FOLD\n")
        elif d.ismedlowhand(self.holecards):
            if 'BET' in self.legalactions:
                input_socket.send("BET:"+self.legalactions['BET'][1]+"\n")
            elif 'RAISE' in self.legalactions and self.raisecount < 2:
                input_socket.send("RAISE:"+self.legalactions['RAISE'][0]+"\n")
            elif 'CALL' in self.legalactions and self.raisecount < 2:
                input_socket.send("CALL:"+self.legalactions['CALL'][0]+"\n")
            else:
                 input_socket.send("FOLD\n")
        elif 'CHECK' in self.legalactions:
            input_socket.send("CHECK\n")
        else:
            input_socket.send("FOLD\n")
    def flop(self, input_socket, d):
        if d.pairorbetter(self.boardcards, self.holecards):
            if d.istophand(self.holecards):
                if 'BET' in self.legalactions:
                    input_socket.send("BET:"+self.legalactions['BET'][1]+"\n")
                elif 'RAISE' in self.legalactions and self.raisecount < 2:
                    input_socket.send("RAISE:"+self.legalactions['RAISE'][1]+"\n")
                elif 'CALL' in self.legalactions:
                    input_socket.send("CALL:"+self.legalactions['CALL'][0]+"\n")
            elif d.ismedhand(self.holecards):
                if 'BET' in self.legalactions:
                    input_socket.send("BET:"+self.legalactions['BET'][1]+"\n")
                elif 'RAISE' in self.legalactions and self.raisecount < 2:
                    input_socket.send("RAISE:"+self.legalactions['RAISE'][1]+"\n")
                elif 'CALL' in self.legalactions and self.raisecount < 3:
                    input_socket.send("CALL:"+self.legalactions['CALL'][0]+"\n")
                else:
                    input_socket.send("FOLD\n")
            elif d.ismedlowhand(self.holecards):
                if 'BET' in self.legalactions:
                    input_socket.send("BET:"+self.legalactions['BET'][0]+"\n")
                elif 'CALL' in self.legalactions and self.raisecount < 2:
                    input_socket.send("CALL:"+self.legalactions['CALL'][0]+"\n")
                else:
                    input_socket.send("FOLD\n")
            elif 'CALL' in self.legalactions and self.raisecount < 2:
                input_socket.send("CALL:"+self.legalactions['CALL'][0]+"\n")
            elif 'BET' in self.legalactions:
                input_socket.send("BET:"+self.legalactions['BET'][0]+"\n")
            else:
                 input_socket.send("FOLD\n")
        elif 'CHECK' in self.legalactions:
            input_socket.send("CHECK\n")
        else:
            input_socket.send("FOLD\n")
    def turn(self, input_socket, d):
        if d.pairorbetter(self.boardcards, self.holecards):
            if d.istophand(self.holecards):
                if 'BET' in self.legalactions:
                    input_socket.send("BET:"+self.legalactions['BET'][1]+"\n")
                elif 'RAISE' in self.legalactions and self.raisecount < 2:
                    input_socket.send("RAISE:"+self.legalactions['RAISE'][1]+"\n")
                elif 'CALL' in self.legalactions:
                    input_socket.send("CALL:"+self.legalactions['CALL'][0]+"\n")
            elif d.ismedhand(self.holecards):
                if 'BET' in self.legalactions:
                    input_socket.send("BET:"+self.legalactions['BET'][1]+"\n")
                elif 'CALL' in self.legalactions and self.raisecount < 2:
                    input_socket.send("CALL:"+self.legalactions['CALL'][0]+"\n")
            elif d.ismedlowhand(self.holecards):
                if 'BET' in self.legalactions:
                    input_socket.send("BET:"+self.legalactions['BET'][0]+"\n")
                elif 'CALL' in self.legalactions:
                    input_socket.send("CALL:"+self.legalactions['CALL'][0]+"\n")
            elif 'CALL' in self.legalactions:
                input_socket.send("CALL:"+self.legalactions['CALL'][0]+"\n")
            elif 'CHECK' in self.legalactions:
                input_socket.send("CHECK\n")
        elif 'CHECK' in self.legalactions:
            input_socket.send("CHECK\n")
        else:
            input_socket.send("FOLD\n")
    def river(self, input_socket, d):
        if d.pairorbetter(self.boardcards, self.holecards):
            if d.istophand(self.holecards):
                if 'BET' in self.legalactions:
                    input_socket.send("BET:"+self.legalactions['BET'][1]+"\n")
                elif 'RAISE' in self.legalactions and self.raisecount < 2:
                    input_socket.send("RAISE:"+self.legalactions['RAISE'][1]+"\n")
                elif 'CALL' in self.legalactions:
                    input_socket.send("CALL:"+self.legalactions['CALL'][0]+"\n")
            elif d.ismedhand(self.holecards):
                if 'BET' in self.legalactions:
                    input_socket.send("BET:"+self.legalactions['BET'][1]+"\n")
                elif 'CALL' in self.legalactions and self.raisecount < 2:
                    input_socket.send("CALL:"+self.legalactions['CALL'][0]+"\n")
            elif d.ismedlowhand(self.holecards):
                if 'BET' in self.legalactions:
                    input_socket.send("BET:"+self.legalactions['BET'][0]+"\n")
                elif 'CALL' in self.legalactions:
                    input_socket.send("CALL:"+self.legalactions['CALL'][0]+"\n")
            elif 'CALL' in self.legalactions:
                input_socket.send("CALL:"+self.legalactions['CALL'][0]+"\n")
            elif 'CHECK' in self.legalactions:
                input_socket.send("CHECK\n")
        elif 'CHECK' in self.legalactions:
            input_socket.send("CHECK\n")
        else:
            input_socket.send("FOLD\n")
    def run(self, input_socket):
        # Get a file-object for reading packets from the socket.
        # Using this ensures that you get exactly one packet per read.
        f_in = input_socket.makefile()
        # initialize the deck
        d = Deck()
        d.initialize()
        # print "Top hands ", Player.d.tophands
        while True:
            # Block until the engine sends us a packet.
            data = f_in.readline().strip()
            # If data is None, connection has closed.
            if not data:
                print "Gameover, engine disconnected."
                break

            # Here is where you should implement code to parse the packets from
            # the engine and act on it. We are just printing it instead.
            print data

            # When appropriate, reply to the engine with a legal action.
            # The engine will ignore all spurious responses.
            # The engine will also check/fold for you if you return an
            # illegal action.
            # When sending responses, terminate each response with a newline
            # character (\n) or your bot will hang!
            packet = data.split()
            word = packet.pop(0)
            self.unpack(word, packet)
            if word == "NEWHAND":
                print "\n------------------------> Hole cards ", self.holecards, "\n"
            elif word == "GETACTION":
                if self.ispreflop():
                    print "pre flop boardcards : ", self.boardcards, " raise count ", str(self.raisecount)
                    print "legal actions", self.legalactions
                    self.preflop(input_socket, d)
                elif self.isflop():
                    print "flop boardcards : ", self.boardcards, " raise count ", str(self.raisecount)
                    print "legal actions", self.legalactions
                    print "pairorbetter ", d.pairorbetter(self.boardcards, self.holecards)
                    self.flop(input_socket, d)
                elif self.isturn():
                    print "turn boardcards : ", self.boardcards, " raise count ", str(self.raisecount)
                    print "legal actions", self.legalactions
                    self.turn(input_socket, d)
                elif self.isriver():
                    print "river boardcards : ", self.boardcards, " raise count ", str(self.raisecount)
                    print "legal actions", self.legalactions
                    self.river(input_socket, d)
                # Currently CHECK on every move. You'll want to change this.
                #s.send("CHECK\n")
            elif word == "REQUESTKEYVALUES":
                # At the end, the engine will allow your bot save key/value pairs.
                # Send FINISH to indicate you're done.
                print "Finishing stack size ", self.stacksizes[self.seat]
                input_socket.send("FINISH\n")
        # Clean up the socket.
        input_socket.close()

