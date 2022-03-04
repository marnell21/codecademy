import random

# Create a Master deck of cards and values
face_cards = ["Ace","King","Queen","Jack"]
suits = ["Hearts", "Spades", "Clubs", "Diamonds"] 
card_values = {}
for i in range(2,11):
    for suit in suits:
        card_values[str(i) + " of " + suit] = i
for face_card in face_cards:
    for suit in suits:
        # Exclude the Ace card, because we will ask the player the value
        if face_card != "Ace":
            card_values[face_card + " of " + suit] = 10

# Create a game deck with the given number of card decks in it
def create_game_deck(number_of_decks=1):
    game_deck = []
    for cnt in range(0,number_of_decks):
        for i in range(2,11):
            for suit in suits:
                game_deck.append(str(i) + " of " + suit)
        for face_card in face_cards:
            for suit in suits:
                game_deck.append(face_card + " of " + suit)
    return game_deck

# Create a player class
class Player:
    def __init__(self, name, money=0):
        self.hand1 = []
        self.hand2 = []
        self.bet1 = 0
        self.bet2 = 0
        self.score1 = 0
        self.score2 = 0
        self.money = money
        self.name = name
        self.current_action = "hit"

    def __repr__(self):
        return "Player is {name} with ${amount} in your wallet. Your current bet is ${bet_amt}".format(name=self.name,amount=self.money,bet_amt=self.bet1+self.bet2)

def create_a_player():
    name = input("Welcome player! What is your name: ")
    money = float(input("How much money do you have? "))
    player1 = Player(name, money)
    return player1

def make_a_bet(player):
    bet_amount = float(input("How much would you like to bet? "))
    if player.bet1 == 0:
        player.bet1 += bet_amount
    else:
        player.bet2 += bet_amount
    player.money -= bet_amount

def shuffle_cards(deck):
    return random.shuffle(deck)

# Function to deal initial cards. Players is a list of players.
def initial_deal(players, deck, used_card_deck, dealers_hand):
    num_players = len(players)
    for i in range(0,2):
        for j in range(0,num_players):
            next_card = deck.pop(0)
            players[j].hand1.append(next_card)
            used_card_deck.append(next_card)
        next_card = deck.pop(0)
        dealers_hand.append(next_card)
        used_card_deck.append(next_card)

# Function to score a hand
def score_hand(hand, dealer=False):
    score = 0
    # Look up the card values
    for card in hand:
        # If the card is not an Ace, look up the value
        if card in card_values:
            score += card_values[card]
        # Assign value for Ace cards
        else:
            # If it's not the dealer, ask the player how to value Ace
            if not dealer:
                ace_value = int(input("Would you like the Ace to be worth 1 or 11? "))
                score += ace_value
            # If it is the dealer, determine how to value the Ace
            else:
                if score + 11 > 21:
                    score += 1
                else:
                    score += 11
    return score

def hit_player(player, deck, used_card_deck, hand_num=1, dealer=False, dealer_hand=[]):
    next_card = deck.pop(0)
    used_card_deck.append(next_card)
    if not dealer:
        if hand_num == 1:
            player.hand1.append(next_card)
        else:
            player.hand2.append(next_card)
    else:
        dealer_hand.append(next_card)

# Function to play blackjack
# Input the number of card decks to use
def play_blackjack(number_of_decks):
    play_game = True
    # Create a game deck of cards with the given number of card decks
    game_deck = create_game_deck(number_of_decks)
    used_cards = []
    shuffle_cards(game_deck)
    #print("We have {number} of cards in our deck.".format(number=len(game_deck)))

    # Create a player
    game_player = create_a_player()
    initial_wallet = game_player.money
    print("\nWelcome to BlackJack {name}!".format(name=game_player.name))
    print("We are playing with {num} decks of cards.\n".format(num=number_of_decks))

    while(play_game == True):
        # Reset player
        game_player.hand1 = []
        game_player.hand2 = []
        game_player.current_action = "hit"

        # Player makes a bet
        print("You currently have ${amount}.".format(amount=game_player.money))
        make_a_bet(game_player)
        print("You have bet ${amount}.\n".format(amount=game_player.bet1))

        # Deal initial cards
        dealers_hand = []
        initial_deal([game_player], game_deck, used_cards, dealers_hand)
        print("Your cards are {cards}.".format(cards=game_player.hand1))
        print("Dealer's first card is {card}\n".format(card=dealers_hand[0]))
        #print("Dealer's cards are {cards}".format(cards=dealers_hand))
        #print("We have used these cards: {cards}. We have {cnt} of cards left".format(cards=used_cards,cnt=len(game_deck)))

        # Determine if dealer or player have a natural blackjack
        player_score = score_hand(game_player.hand1)
        dealer_score = score_hand(dealers_hand,dealer=True)
        print("Your current score is {score}.".format(score=player_score))
        #print("Dealer has a score of: {score}".format(score=dealer_score))
        if player_score == 21:
            if dealer_score == 21:
                print("Player and Dealer have Blackjack. We have a stand-off. Player keeps their bet.\n")
                game_player.money += game_player.bet1
                game_player.bet1 = 0
            else:
                print("Player has Blackjack and has won! You receive ${winnings}.\n".format(winnings=game_player.bet1*1.5))
                game_player.money += game_player.bet1*1.5
                game_player.money += game_player.bet1
                game_player.bet1 = 0
            print("You have ${winnings} in winnings and ${money} total.\n".format(winnings=game_player.money-initial_wallet,money=game_player.money))
            continue_game = input("Would you like to play again? (Yes/No) ")
            if continue_game.lower() == "yes":
                continue
            else:
                print("Thanks for playing Blackjack!")
                break
        elif dealer_score == 21:
            print("Dealer has Blackjack. Player forfeits bet.")
            game_player.bet1 = 0
            print("You have ${winnings} in winnings for ${money} total.\n".format(winnings=game_player.money-initial_wallet,money=game_player.money))
            continue_game = input("Would you like to play again? (Yes/No) ")
            if continue_game.lower() == "yes":
                continue
            else:
                print("Thanks for playing Blackjack!")
                break
        else:
            print("Game moves to player")

        # Move to player to determine action until player stands or busts
        while game_player.current_action != "stand":
            player_move = input("\nWould you like to Hit or Stand? ")
            if player_move.lower() == "hit":
                hit_player(game_player, game_deck, used_cards)
                print("\nYou drew a {new_card}. Your cards are {cards}.".format(new_card=game_player.hand1[-1],cards=game_player.hand1))
                player_score = score_hand(game_player.hand1)
                print("Your current score is: {score}".format(score=player_score))
                if player_score > 21:
                    print("Player busts.")
                    game_player.bet1 = 0
                    game_player.current_action = "stand"    
            elif player_move.lower() == "stand":
                game_player.current_action = "stand"

        # When player is done, dealer plays
        print("\nDealer's cards are {cards} with a score of {score}.".format(cards=dealers_hand,score=dealer_score))
        while dealer_score < 17:
            print("Dealer will draw.\n")
            hit_player(None, game_deck, used_cards, dealer=True, dealer_hand=dealers_hand)
            dealer_score = score_hand(dealers_hand,dealer=True)
            print("Dealer's cards are {cards} with a score of {score}.\n".format(cards=dealers_hand, score=dealer_score))
        if dealer_score <= 21:
            print("Dealer stands with a score of {score}. We will now settle.\n".format(score=dealer_score))
        else:
            print("Dealer busts with a score of {score}. We will now settle.\n".format(score=dealer_score))

        # Settle with players
        if dealer_score > 21:
            if player_score > 21:
                print("Dealer busted and player busted. Player lost amount of their bet.\n")
            if player_score <= 21:
                print("Dealer busted. Player wins the amount of their bet.\n")
                game_player.money += 2 * game_player.bet1
                game_player.bet1 = 0
        else:
            if dealer_score > player_score:
                print("Dealer beat player. Player loses bet.\n")
                game_player.bet1 = 0
            elif player_score > dealer_score and player_score <= 21:
                print("Player beat dealer and wins amount of bet.\n")
                game_player.money += 2 * game_player.bet1
                game_player.bet1 = 0
            elif player_score == dealer_score:
                print("Player and dealer tie. Bets are a stand-off.\n")
                game_player.money += game_player.bet1
                game_player.bet1 = 0
            elif player_score > 21:
                print("Player busted and lost bet.\n")
        print("You have ${winnings} in winnings for ${money} total.\n".format(winnings=game_player.money-initial_wallet,money=game_player.money))
        continue_game = input("Would you like to play again? (Yes/No) ")
        if continue_game.lower() == "yes":
            continue
        else:
            print("\nThanks for playing Blackjack!")
            break


play_blackjack(6)