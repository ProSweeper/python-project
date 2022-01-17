import random
import os
from syslog import LOG_CRIT
SUITS = ("HEARTS", "SPADES", "CLUBS", "DIAMONDS")
SYMBOLS = ('♥', '♠', '♣', '♦')


def clear():
    os.system('clear')


def get_deck():
    """ Gets the deck of cards and shuffles it using the random module. The cards will be a tuple of the value and suit"""
    deck = []
    for symbol in SYMBOLS:
        for num in range(2,11):
            card = (str(num), symbol)
            deck.append(card)
        for char in ("J", "Q", "K", "A"):
            card = ((char, symbol))
            deck.append(card)
    random.shuffle(deck)
    return deck


def get_bet():
    """get the bet from the player"""
    # print(f'Bank: ${bank}')
    valid_bet = False
    while not valid_bet:
        try:
            bet_amount = int(input("How much would you like to bet?\n$"))
            if 1 <= bet_amount <= bank:
                # print(f"Bet: ${bet}")
                return bet_amount
            else:
                print('Not enough money in your bank')
        except ValueError:
            print("Please enter a valid bet")


def show_cards(cards):
    table = ['', '', '', '', '']
    for card in cards:
        table[0] += ' ___ '
        if card == 'back':
            table[1] += f'|## |'
            table[2] += f'|###|'
            table[3] += f'|_##|'
        elif card[0] == 10:
            table[1] += f'|{card[0]} |'
            table[2] += f'| {card[1]} |'
            table[3] += f'|_{card[0]}|'
        elif card != 'back' and card[0] != 10:
            table[1] += f'|{card[0]}  |'
            table[2] += f'| {card[1]} |'
            table[3] += f'|__{card[0]}|'
    for item in table:
        print(item)


def show_hands(player_hand, dealer_hand, dealers_turn):
    if dealers_turn:
        print(f"Dealer's Hand: {hand_value(dealer_hand)}\n")
        show_cards(dealer_hand)
    else:
        print("Dealers Hand: ???\n")
        show_cards(['back'] + [dealer_hand[-1]])
    print("\n")
    print(f"Your Hand: {hand_value(player_hand)}")
    show_cards(player_hand)


def get_player_move():
    """Ask the player if they want to (H)it, (S)tand, or (D)ouble down if they are able to."""
    moves = ["S", "H", "HIT", "STAND"]
    prompt = "Would you like to (H)it or (S)tand? "
    initial_prompt = "Would you like to (H)it, (S)tand, or (D)ouble down "
    while True:
        if len(player_hand) == 2:
            moves.append("D")
            moves.append("DOUBLE DOWN")
            player_choice = input(initial_prompt).upper()
        else:
            player_choice = input(prompt).upper()
        if player_choice in moves:
            return player_choice
        else:
            print("Please enter a valid move")


def hand_value(player_hand):
    hand_value =0
    aces_in_hand = 0
    for card in player_hand:
        card_type = card[0]
        if card_type == 'A':
            aces_in_hand += 1
        elif card_type in ["J", "Q", "K"]:
            hand_value += 10
        else:
            hand_value += int(card_type)
    hand_value += aces_in_hand
    for i in range(aces_in_hand):
        if hand_value + 10 <= 21:
            hand_value += 10
    return hand_value


def dealer_turn(dealer_hand):
  dealer_turn = True
  while dealer_turn:  
    show_hands(player_hand, dealer_hand, True)
    if hand_value(dealer_hand) >= 21:
        dealer_turn = False
    elif hand_value(dealer_hand) < 17:
        print('The dealer draws a card')
        dealer_hand.append(deck.pop())
        turn = input("Press enter to continue")
    elif hand_value(dealer_hand) >= 17:
        print("The dealer stands")
        dealer_turn = False

clear()
bank = 3000 # starting money amount
while True:    
    clear()
    print(f"Bank: ${bank}")
    player_hand = []
    dealer_hand = []

    if bank > 0:
        bet = get_bet()
        bank -= bet
    else:
        break
    next = input(f"Your bet is ${bet}, press enter to continue")
    player_bust = False
    dealer_bust = False
    player_blackjack = False
    dealer_blackjack = False
    deck = get_deck()
    dealer_hand = [deck.pop(), deck.pop()]
    player_hand = [deck.pop(), deck.pop()]
    # show_hands(player_hand, dealer_hand, False)
    player_turn = True
    while player_turn:
        clear()
        print(f"Bank: ${bank}")
        show_hands(player_hand, dealer_hand, False)
        if hand_value(player_hand) == 21 and len(player_hand) == 2:
            player_blackjack = True
            bet *= 1.5
            player_turn = False
        elif hand_value(player_hand) == 21:
            player_turn = False
            print("Stand, it's the dealer's turn")
        else:
            move = get_player_move()
            if move in ['H', 'HIT']:
                print("Hit, the dealers deals you a card")
                player_hand.append(deck.pop())
                show_hands(player_hand, dealer_hand, False)
                if hand_value(player_hand) > 21:
                    print("BUST! Dealer wins")
                    player_bust = True
                    player_turn = False
            elif move in ['S', 'STAND']:
                print("Stand, its the dealers turn")
                player_turn = False
            elif move in ['D', 'DOUBLE DOWN']:
                print('Double down, your bet is doubled and the dealer deals you a card')
                bank -= bet
                bet *= 2
                player_hand += deck.pop()
                if hand_value(player_hand) > 21:
                    player_bust = True
                    print("BUST! Dealer wins")
                player_turn = False
    if player_bust == False:
        print("_____________________________")
        print("The dealer shows their card")
        show_hands(player_hand, dealer_hand, True)
        next = input("Press enter to continue")
        if hand_value(dealer_hand) == 21 and len(dealer_hand) == 2:
            dealer_blackjack = True
        if dealer_blackjack == True and player_blackjack == False:
            print("Dealer Blackjack, you lose")
        elif dealer_blackjack == True and player_blackjack == True:
            print("It's a draw, push")
        elif dealer_blackjack == False and player_blackjack == True:
            print("BLACKJACK, YOU WIN!")
            bank += bet * 2
            print(f"${bet * 2} added to bank")
        else:
            dealer_turn(dealer_hand)
            if hand_value(dealer_hand) > 21:
                dealer_bust = True
                print("Dealer busts, YOU WIN!")
            if dealer_bust == True:
                bank += bet * 2
                print(f"${bet * 2} added to bank")
            elif hand_value(dealer_hand) > hand_value(player_hand):
                print('Dealer wins, better luck next hand')
            elif hand_value(dealer_hand) < hand_value(player_hand):
                print("You win")
                bank += bet * 2
                print(f"${bet * 2} added to bank")
            elif hand_value(dealer_hand) == hand_value(player_hand):
                print("It's a draw, push")
                bank += bet
                print(f"${bet} added back to bank")
    next_turn = input("Press enter for next turn")
