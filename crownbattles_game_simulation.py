import random

class Card:
    owner = None
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

    def __str__(self):
        return self.suit + '-' + str(self.number)

class Player:
    def __init__(self, id):
        self.id = id
        self.hand = []

    def add_card(self, card):
        card.owner = self.id
        self.hand.append(card)

    def play_card(self, leading_suit):
        if leading_suit is None:
            card = random.choice(self.hand)
            return card
        # If player has a card of the leading suit, must play it.
        leading_suit_cards = [card for card in self.hand if card.suit == leading_suit]
        if leading_suit_cards:
            # logic: play the highest card from hand
            card = max(leading_suit_cards, key=lambda c: c.number)
        else:
        # If not play a random card
            card = random.choice(self.hand)
        self.hand.remove(card)
        return card


def prepare_and_shuffle_deck():
    deck = []
    suits = ['Red', 'Green', 'Blue', 'Yellow']
    numbers = range(1, 14)
    for _ in range(2):  # Two G cards
        deck.append(Card('G', 0))
    for _ in range(2):  # Two D cards
        deck.append(Card('D', 0))
    for _ in range(4):  # Four P cards
        deck.append(Card('P', 0))
    for suit in suits:
        for number in numbers:
            deck.append(Card(suit, number))

    random.shuffle(deck)
    return deck

def deal_cards(deck, num_players, num_cards):
    players = [Player(i) for i in range(num_players)]
    for _ in range(num_cards):
        for player in players:
            player.add_card(deck.pop())

    return players


def determine_trick_winner(leading_suit, cards, trump_suit):

    dragons = [card for card in cards if card.suit == 'D']
    if dragons:
        return dragons[0]
    
    golems = [card for card in cards if card.suit == 'G']
    if golems:
        return golems[0]
    
    trump_suit_cards = [card for card in cards if card.suit == trump_suit]
    if trump_suit_cards:
        biggest_trump_suit_no = max(trump_suit_cards, key=lambda c: c.number)
        return biggest_trump_suit_no

    leading_suit_cards = [card for card in cards if card.suit == leading_suit]
    if leading_suit_cards:
        # print('all leading_suit_cards:')
        # print(*leading_suit_cards)
        biggest_leading_no = max(leading_suit_cards, key=lambda c: c.number)
        # print('biggest_leading_no:')
        # print(biggest_leading_no)
        return biggest_leading_no
    
    peasant_cards = [card for card in cards if card.suit == 'P']
    if peasant_cards:
        return peasant_cards[0]

def play_game(num_players, num_cards_for_the_round):
    trick_pile_cards = []
    leading_suit = None
    player_wins = [0] * num_players

    deck = prepare_and_shuffle_deck()
    players = deal_cards(deck, num_players, num_cards_for_the_round)

    # print(f'Finished dealing cards. Here are the hands of each player:')
    # for player in players:
    #     print(f'player {player.id} has hand')
    #     print(*player.hand)

    trump_suit = random.choice(['Red', 'Green', 'Blue', 'Yellow'])
    # print(f'Trump suit for the round is {trump_suit}')

    for _ in range(num_cards_for_the_round):
        # print('Starting a new trick. Resetting the trick')
        # re-setting the leading suit
        leading_suit = None
        # re-setting (Empty) the pile trick_pile_cards
        trick_pile_cards = []
        # New trick starting. All players play a card for this trick
        for player in players:
            card = player.play_card(leading_suit)
            # If there is no leading suit already 
            if leading_suit is None and card.suit not in ['P', 'G', 'D']: # TODO: if G or D there is no leading suit
                leading_suit = card.suit
            # print(f'player {player.id} plays this card {card}')
            trick_pile_cards.append(card)

        # print(f'These are this trick''s piled cards:')
        # print(*trick_pile_cards)
        # print(f'And the leading_suit played was {leading_suit}')
        winner = determine_trick_winner(leading_suit, trick_pile_cards, trump_suit)
        # print(f'Winner card is {winner}')
        if winner:
            # find the player who played the winning card
            player_wins[winner.owner] += 1

        # re-arrange players, winning players goes first
        players = players[winner.owner:] + players[:winner.owner]
        # print(f'player wins are')
        # print(*player_wins)
    return player_wins[0] # Return any of the players


num_simulations = 100
num_players_list = [2,3,4,5,6,7,8]
# Key is the number of players, value is a list of the cards to deal on each round
num_cards_for_the_round_dict = {} 
num_cards_for_the_round_dict[2] = [2,4,6,8,10,12,14,16,18,20]   # 2-players
num_cards_for_the_round_dict[3] = [2,4,6,8,10,12,14,16,18,20]   # 3-players
num_cards_for_the_round_dict[4] = [1,3,5,7,9,11,13,15]          # 4-players
num_cards_for_the_round_dict[5] = [1,2,3,4,5,6,7,8,9,10,11,12]  # 5-players
num_cards_for_the_round_dict[6] = [1,2,3,4,5,6,7,8,9,10]        # 6-players
num_cards_for_the_round_dict[7] = [1,2,3,4,5,6,7,8]             # 7-players
num_cards_for_the_round_dict[8] = [1,2,3,4,5,6,7]               # 8-players
# How many times did a player meet the target? i.e win exactly 2 tricks
count_target_met = 0   
# Target of the game
target_tricks_won_list = [0,1,2,3,4]

for num_players in num_players_list:
    for num_cards_for_the_round in num_cards_for_the_round_dict[num_players]:
        for target_tricks_won in target_tricks_won_list:
            for i in range(num_simulations):
                player1_tricks_won = play_game(num_players, num_cards_for_the_round)
                
                if player1_tricks_won == target_tricks_won:
                    count_target_met += 1

            probability = count_target_met / num_simulations
            print(f"The probability of winning exactly {target_tricks_won} tricks " \
                  f"in a {num_players}-player game " \
                f"each having {num_cards_for_the_round} cards on hand is: {probability*100:.2f}%")
            count_target_met = 0 # reset the number of target was met variable in the game