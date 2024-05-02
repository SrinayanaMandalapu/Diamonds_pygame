import os
import random
from strategy import ComputerStrategy
#from ui import UI

class Game:
    def __init__(self, num_players, against_computer):
        self.num_players = num_players
        self.against_computer = against_computer

    def start(self):
        running = True
        while running:
            if self.num_players not in [1, 2, 3]:
                print("Invalid number of players. Please enter 1, 2, or 3.")
                continue
            players_cards = self.distribute_cards()
            diamond_cards = []
            scores = {f"Player {i + 1}": 0 for i in range(self.num_players)}  # Initialize scores
            if self.against_computer:
                players_cards, computers_cards = self.distribute_cards()
            while diamond_cards:
                for round_num in range(1, 14):
                    highest_bid = {player: None for player in players_cards}
                    diamond_card = self.select_diamond_card()
                    for player, cards in players_cards.items():
                        bidding_card = self.bidding_round(player, cards)
                        if bidding_card in cards:
                            highest_bid[player] = bidding_card
                            players_cards[player].remove(bidding_card)
                    if self.against_computer:
                        computers_bid = self.computers_bid_strategy(players_cards, computers_cards, diamond_card, diamond_cards)
                        highest_bid["computer"] = computers_bid
                        computers_cards.remove(computers_bid)
                    card_values = {
                        "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
                        "jack": 11, "queen": 12, "king": 13, "ace": 14
                    }
                    max_bid_value = max(highest_bid.values(), key=lambda x: card_values.get(x.split("_")[0]))
                    players_with_max_bid = [player for player, bid in highest_bid.items() if bid.split()[0] == max_bid_value.split()[0]]
                    diamonds_earned = 0
                    if players_with_max_bid:
                        if len(players_with_max_bid) == 1:
                            if isinstance(diamond_card, int):
                                diamonds_earned = diamond_card
                            else:
                                if diamond_card == "ace":
                                    diamonds_earned = 14
                                elif diamond_card == "king":
                                    diamonds_earned = 13
                                elif diamond_card == "queen":
                                    diamonds_earned = 12
                                elif diamond_card == "jack":
                                    diamonds_earned = 11
                                else:
                                    diamonds_earned = int(diamond_card.split("_")[0])
                            scores[players_with_max_bid[0]] += diamonds_earned
                        else:
                            if isinstance(diamond_card, int):
                                diamonds_earned_per_player = diamond_card / len(players_with_max_bid)
                            else:
                                if diamond_card == "ace":
                                    diamonds_earned_per_player = 14 / len(players_with_max_bid)
                                elif diamond_card == "king":
                                    diamonds_earned_per_player = 13 / len(players_with_max_bid)
                                elif diamond_card == "queen":
                                    diamonds_earned_per_player = 12 / len(players_with_max_bid)
                                elif diamond_card == "jack":
                                    diamonds_earned_per_player = 11 / len(players_with_max_bid)
                                else:
                                    diamonds_earned_per_player = int(diamond_card.split("_")[0]) / len(players_with_max_bid)
                            for player in players_with_max_bid:
                                scores[player] += diamonds_earned_per_player
                            diamonds_earned = diamonds_earned_per_player * len(players_with_max_bid)
                    else:
                        diamonds_earned = 0
            winner = max(scores, key=scores.get)
            print(f"{winner} wins with {scores[winner]} diamonds!")

    def distribute_cards(self):
        suits = ["clubs", "hearts", "spades", "diamonds"]
        random.shuffle(suits)
        players_cards = {f"Player {i + 1}": [] for i in range(self.num_players)}
        card_names = [
            "2_of_clubs", "3_of_clubs", "4_of_clubs", "5_of_clubs", "6_of_clubs", "7_of_clubs", "8_of_clubs",
            "9_of_clubs", "10_of_clubs", "jack_of_clubs", "queen_of_clubs", "king_of_clubs", "ace_of_clubs",
            "2_of_hearts", "3_of_hearts", "4_of_hearts", "5_of_hearts", "6_of_hearts", "7_of_hearts", "8_of_hearts",
            "9_of_hearts", "10_of_hearts", "jack_of_hearts", "queen_of_hearts", "king_of_hearts", "ace_of_hearts",
            "2_of_spades", "3_of_spades", "4_of_spades", "5_of_spades", "6_of_spades", "7_of_spades", "8_of_spades",
            "9_of_spades", "10_of_spades", "jack_of_spades", "queen_of_spades", "king_of_spades", "ace_of_spades",
            "2_of_diamonds", "3_of_diamonds", "4_of_diamonds", "5_of_diamonds", "6_of_diamonds", "7_of_diamonds",
            "8_of_diamonds", "9_of_diamonds", "10_of_diamonds", "jack_of_diamonds", "queen_of_diamonds",
            "king_of_diamonds",
            "ace_of_diamonds"
        ]
        for i in range(self.num_players):
            for card_name in card_names[i * 13: (i + 1) * 13]:
                players_cards[f"Player {i + 1}"].append(card_name)
        if not self.against_computer:
            return players_cards
        computers_cards = []
        for card_name in card_names[2 * 13: (3) * 13]:
            computers_cards.append(card_name)
        return players_cards, computers_cards

    def bidding_round(self, player, cards):
        bidding_card = None
        running = True
        while running:
            # Bidding logic goes here
            print(f"{player}'s turn to bid.")
            print(f"Click on the card you want to bid:")
            for i, card_name in enumerate(cards):
                print(f"{i + 1}. {card_name}")
            choice = input("Enter the number corresponding to your bid: ")
            if choice.isdigit() and 1 <= int(choice) <= len(cards):
                bidding_card = cards[int(choice) - 1]
                running = False
            else:
                print("Invalid input. Please enter a number corresponding to your bid.")
        return bidding_card

    def select_diamond_card(self):
        diamond_cards = list(range(2, 11)) + ["jack", "queen", "king", "ace"]
        random.shuffle(diamond_cards)
        return diamond_cards.pop()

    def determine_winner(self, scores):
        winner = max(scores, key=scores.get)
        return winner

    def computers_bid_strategy(self, players_cards, computers_cards, diamond_card, remaining_diamond_cards):
        # Implement computer's bidding strategy here
        if remaining_diamond_cards:
        # Filter out non-numeric values from remaining_diamond_cards
            remaining_diamond_values = [card for card in remaining_diamond_cards if isinstance(card, int)]
        
        # Check if there are any remaining diamond values after filtering
        if remaining_diamond_values:
            # Get the value of the diamond card to be bid on
            diamond_value = get_card_value(diamond_card)
            
            # Calculate the average value of the remaining diamond cards
            average_diamond_value = sum(remaining_diamond_values) / len(remaining_diamond_values)
            
            # Determine the threshold for bidding based on the average value of remaining diamond cards
            bidding_threshold = average_diamond_value * 0.8  # Adjust as needed
            
            # Evaluate the player's hand and select the best card to bid
            best_card = evaluate_best_bid(computers_cards, diamond_value, bidding_threshold, remaining_diamond_values)
            
            return best_card

    # If there are no remaining diamond cards, bid the lowest card in the computer's hand
        return min(computers_cards, key=lambda x: get_card_value(x))
