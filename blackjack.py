import random

DEBUG=1

# Strategy - should export an "Evaluate Hand" function
# evaluateHand( hand, surrender ) -- returns hit/stand/double/split

suits = [ "hearts", "diamonds", "clubs", "spades"]
cards = [ 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
card_value = {
    2  : 2,
    3  : 3,
    4  : 4,
    5  : 5,
    6  : 6,
    7  : 7,
    8  : 8,
    9  : 9,
    10 : 10,
    "J" : 10,
    "Q" : 10,
    "K" : 10,
    "A" : 11,
}
# TODO: Add Surrender
legal_moves = [ "H", "S", "D", "Q" ]
legal_long_moves = ["Hit","Stand", "Split", "Double", "Quit" ]


class Card:
    value = 0
    suit = "none"

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def getValue(self):
        return card_value[self.value]

    def getCardString(self):
        return str(self.value) + " of " + str(self.suit)

def generateHand( deck, cards=2 ):
    # could be done with list comprehension?
    hand = []
    for i in range(0,cards):
        hand.append(deck.pop())
    return hand

def shuffleDeck( deck ):
    return random.shuffle(deck)

def createDeck(decks):
    deck = []
    for i in range(0,decks):
        for suit in suits:
            for card in cards:
                deck.append( Card(card,suit) )
    shuffleDeck(deck)

    return deck

def showGameState(player, dealer, deck):
    # FIXME: Clear screen instead
    for i in range(0,25):
        print "\n"

    print "Cards left: " + str(len(deck))
    print "DEALER: "
    print ""
    print dealer[0].getCardString()
    print "\n\n\n"
    print "PLAYER: "
    print ""
    for c in player:
        print c.getCardString()
    print ""
    # TODO: calculate and show totals?


def getPlayerMove():
    move = 0
    while move == 0:
        move = raw_input("Your move? [H,S,D,Split] > ")

        if move not in [x.lower() for x in legal_moves] and move not in [y.lower() for y in legal_long_moves]:
            print "Illegal move"
            move = 0
    return move

def getHandTotal(hand):
    total = 0
    soft = False

    for c in hand:
        if c.getValue() == 11:
            if total < 11:
                soft = True
            else:
                total += 1
                continue
        total += c.getValue()
    return (total, soft)

low_splits = [2,3,6,7,9]
always_splits = [8,"A"]
high_splits = []

def findBestMove(player,dealer):
    # TODO: Add surrender
    strategy_mid = 6
    # dealer up card is card 0
    dealer_value = dealer[0].getValue()
    (player_total, player_soft) = getHandTotal(player)
    
    if DEBUG:
        ss = "Hard"
        if player_soft: ss = "Soft"
        print "(" + ss + " " + str(player_total) + ")"
        print "(D: " + str(dealer_value) + ")"

    # check splits
    if len(player) == 2 and player[0].value == player[1].value:
        if player[0].value in always_splits:
            return "Split"

        if dealer_value <= strategy_mid:
            if player[0].value in low_splits:
                return "Split"
        else:
            if player[0].value in high_splits:
                return "Split"


    # SOFT
    if player_soft:

        # DEALER HIGH
        if dealer_value > strategy_mid:
            if player_total < 19:
                return "Hit"
            else:
                return "Stand"
        # DEALER LOW
        else:
            if player_total >= 16 and player_total <= 18:
                return "Double"
            if player_total < 16:
                    return "Hit"
            elif player_total > 18:
                    return "Stand"

    # HARD
    else:
        if (player_total == 10 or player_total == 11) and player_total > dealer_value:
            return "Double"
 
        # DEALER HIGH
        if dealer_value > strategy_mid:
            if player_total < 17:
                return "Hit"
            else:
                return "Stand"
        # DEALER LOW
        else:
            if player_total >= 12:
                return "Stand"
            elif player_total < 9:
                    return "Hit"
            elif player_total == 9:
                    return "Double"

    return "Oops!"
       

def print_score( score, best_score, print_words=True ):
    if print_words:
        print "Score: " + str(score) + "/" + str(best_score)
    else:
        print str(score) + "/" + str(best_score)


def play(decks, cut):
    deck = createDeck(decks)
    score = 0
    best_score = 0

    while len(deck) > cut:
        player = generateHand(deck)
        dealer = generateHand(deck,1)

        showGameState(player, dealer, deck)
        if getHandTotal(player)[0] == 21:
            if getHandTotal(dealer)[0] != 21:
                print "BLACKJACK!"
            else:
                print "Push (double blackjack)"
            print_score(score,best_score)
            raw_input("Press enter")
            continue
            
        move = getPlayerMove()

        best_move = findBestMove(player, dealer)

        if move in legal_long_moves and move != "Split":
            move = move[0].lower()

        if move == "q":
            return
        if move == best_move[0].lower():
            print "Correct!"
            score += 1
        else:
            print "Incorrect. The best move was:"
            print str(best_move)
        best_score += 1
        print_score(score,best_score)
        raw_input("Press enter")

    print "Game over. Final score:"
    print_score(score,best_score,False)

        
play(2,15)
