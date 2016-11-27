ranks = {}
# rank['A'] = 14
# rank['K'] = 13
# rank['Q'] = 12
# rank['J'] = 11
# rank['T'] = 10
# for i in range(9, 1, -1):
#     rank[str(i)] = i
suits = {}
suits['c'] = 0.4
suits['d'] = 0.3
suits['h'] = 0.2
suits['s'] = 0.1

rank = ('A','K','Q','J','T','9','8','7','6','5','4','3','2')
suit = ('s','h','d','c')
d = []
for r in rank:
    for s in suit:
        d.append(r+s)
        if r=='A':
            ranks[r+s]=14
        elif r=='K':
            ranks[r+s]=13
        elif r=='Q':
            ranks[r+s]=12
        elif r=='J':
            ranks[r+s]=11
        elif r=='T':
            ranks[r+s]=10
        else:
            ranks[r+s]=int(r) 

def compare(item1, item2):
        return cmp(ranks[item1]+suits[item1[1]], ranks[item2]+suits[item2[1]])
