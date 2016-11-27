import itertools
import Utils

class Deck:
    def __init__(self):
        self.tophands = []
        self.medhands = []
        self.medlowhands = []
        self.lowhands = []
        self.ranks = Utils.ranks
    def compare(item1, item2):
        return cmp(self.rank[item1[0]]+self.suit[item1[1]], self.rank[item2[0]]+self.suit[item2[1]])
    def exists(self, hands, hand):
        hand = sorted(hand, cmp=Utils.compare, reverse=True)
        return hands.count(hand)>0
    def istophand(self, hand):
        return self.exists(self.tophands, hand)
    def ismedhand(self, hand):
        return self.exists(self.medhands, hand)
    def ismedlowhand(self, hand):
        return self.exists(self.medlowhands, hand)
    def islowhand(self, hand):
        return self.exists(self.lowhands, hand)
    def cardnum(self, card):
        return card[0]
    def cardsuit(self, card):
        return card[1]
    def ispicture(self, card):
        return self.cardnum(card) in ('A','K','Q','J')
    def ispocketpair(self, hand):
        return self.cardnum(hand[0]) == self.cardnum(hand[1])
    def pairorbetter(self, board, hand):
        return sum([mycard[0]==boardcard[0] for mycard in hand for boardcard in board],hand[0][0]==hand[1][0]) > 0
    def initialize(self):
        deck = Utils.d
        #print deck
        # create all possible hole card combinations (1326)
        self.poshands=list(itertools.combinations(deck,2))
        self.hands = []
        #print self.hands
        for hand in self.poshands:
            self.hands.append(sorted(hand, cmp=Utils.compare, reverse=True))

        # populate top/med/low hands, to be used in determining (mostly preflop) strategy
        for hand in self.hands:
            if (self.ispicture(hand[0]) and self.ispocketpair(hand)) or (self.cardnum(hand[0])=='A' and self.cardnum(hand[1])=='K'):
                self.tophands.append(hand)
            elif (self.cardnum(hand[0])=='A' and (self.ispicture(hand[1]) or self.cardnum(hand[1]) in ('T','9'))) or (self.ispocketpair(hand) and self.cardnum(hand[0]) in ('T','9')):
                self.medhands.append(hand)
            elif (self.cardnum(hand[0])=='A' or self.ispocketpair(hand) or (self.ispicture(hand[0]) and self.ispicture(hand[1]))):
                self.medlowhands.append(hand)
            else:
                self.lowhands.append(hand)