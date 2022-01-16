import random
SUITS = ("HEARTS", "SPADES", "CLUBS", "DIAMONDS")


def get_deck():
        deck = []
        for suit in SUITS:
            for num in range(2,11):
                card = (str(num), suit)
                deck.append(card)
            for char in ("J", "Q", "K", "A"):
                card = ((char, suit))
                deck.append(card)
        random.shuffle(deck)
        return deck

def deal_cards():
    global player_hand, dealer_hand
    player_hand += [deck.pop(), deck.pop()]
    dealer_hand += [deck.pop(), deck.pop()]


deck = get_deck()
player_hand = []
dealer_hand = []
deal_cards()
print(player_hand)