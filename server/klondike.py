import random


# BUILD CARDS
class Card:
    def __init__(self, value: int, suit: str, flipped: bool = False):
        self.value = value
        self.suit = suit
        self.flipped = flipped

    def __repr__(self):
        """Debug card show stuff"""
        return f'|{self.value}{self.suit}|'


# SUITS = ['hearts', 'diamonds', 'spades', 'clubs']
# SUITS = ['h', 'd', 's', 'c']
SUITS = ['♡', '♢', '♠', '♣']

DECK = [Card(value, suit) for value in range(1, 14) for suit in SUITS]


# PRINT FUNCTIONS
def printdeck():
    for card in DECK:
        print(card.value, card.suit)


def printstock():
    for card in stock:
        print(card.value, card.suit)


def printpile():
    for card in pile:
        print(card.value, card.suit)


def printtableau(tableau):
    for card in tableau:
        if not card.flipped:
            print('|#', end='')
        else:
            print('|', card.value, card.suit, '|', end='', sep='')


def printfoundation(foundation):
    if len(foundation) > 0:
        print('|', foundation[-1].value, foundation[-1].suit, '|\t', end='', sep='')
    else:
        print('|  |\t', end='', sep='')


def printtable():
    printfoundation(foundation4); printtableau(tableau7); print()
    printfoundation(foundation3); printtableau(tableau6); print()
    printfoundation(foundation2); printtableau(tableau5); print()
    printfoundation(foundation1); printtableau(tableau4); print()
    print('    ', '\t', end=''); printtableau(tableau3); print()
    print('|' + str(pile[-1].value) if len(pile) > 0 else '  ', pile[-1].suit + '|' if len(pile) > 0 else '  ', '\t', end='', sep=''); printtableau(tableau2); print()
    print('|##|' if len(stock) > 0 else '|  |', '\t', end='', sep=''); printtableau(tableau1); print("\n")


# BUILD STACKS
stock = DECK[:24]
for card in stock:
    card.flipped = True
pile = []

foundation1 = []
foundation2 = []
foundation3 = []
foundation4 = []

tableau1 = DECK[24:25]; tableau1[-1].flipped = True
tableau2 = DECK[25:27]; tableau2[-1].flipped = True
tableau3 = DECK[27:30]; tableau3[-1].flipped = True
tableau4 = DECK[30:34]; tableau4[-1].flipped = True
tableau5 = DECK[34:39]; tableau5[-1].flipped = True
tableau6 = DECK[39:45]; tableau6[-1].flipped = True
tableau7 = DECK[45:52]; tableau7[-1].flipped = True

tableaus = [pile, tableau1, tableau2, tableau3, tableau4, tableau5, tableau6, tableau7, foundation1, foundation2, foundation3, foundation4]


# MOVE FUNCTIONS
def draw():
    if len(stock) == 0:
        for i in range(len(pile)):
            stock.append(pile.pop(-1))
    elif len(stock) >= 3:
        for i in range(3):
            pile.append(stock.pop(-1))
    else:
        for i in range(len(stock)):
            pile.append(stock.pop(-1))


def move(card_nr_from_bottom, tableau_from, tableau_to):
    for i in range(-card_nr_from_bottom, 0):
        tableaus[tableau_to].append(tableaus[tableau_from].pop(i))
        if len(tableaus[tableau_from]) > 0:
            tableaus[tableau_from][-1].flipped = True


# GAME
def moveinput(turn):
    move(int(turn[0]), int(turn[1]), int(turn[2]))
    printtable()


if __name__ == "__main__":
    random.shuffle(DECK)
    printtable()
    while True:
        turn = input("draw (d) / move (card_from_to): ")

        if turn == "d":
            draw()
            printtable()
        else:
            moveinput(turn)
