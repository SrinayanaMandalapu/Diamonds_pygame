import random

class ComputerStrategy:
    def __init__(self):
        pass

    def bid(self, players_cards, computers_cards, diamond_card, remaining_diamond_cards):
        if remaining_diamond_cards:
            # Filter out non-numeric values from remaining_diamond_cards
            remaining_diamond_values = [card for card in remaining_diamond_cards if isinstance(card, int)]
            
            # Check if there are any remaining diamond values after filtering
            if remaining_diamond_values:
                # Get the value of the diamond card to be bid on
                diamond_value = self.get_card_value(diamond_card)
                
                # Calculate the average value of the remaining diamond cards
                average_diamond_value = sum(remaining_diamond_values) / len(remaining_diamond_values)
                
                # Determine the threshold for bidding based on the average value of remaining diamond cards
                bidding_threshold = average_diamond_value * 0.8  # Adjust as needed
                
                # Evaluate the computer's hand and select the best card to bid
                best_card = self.evaluate_best_bid(computers_cards, diamond_value, bidding_threshold, remaining_diamond_values)
                
                return best_card

        # If there are no remaining diamond cards, bid the lowest card in the computer's hand
        return min(computers_cards, key=lambda x: self.get_card_value(x))

    def evaluate_best_bid(self, cards, diamond_value, bidding_threshold, remaining_diamond_cards):
        # Calculate the percentage of remaining diamond cards below the bidding threshold
        low_value_percentage = len([card for card in remaining_diamond_cards if card < bidding_threshold]) / len(remaining_diamond_cards)
        
        # Adjust the bidding threshold based on the percentage of low-value diamond cards remaining
        adjusted_threshold = bidding_threshold * (1 + (1 - low_value_percentage) * 0.2)  # Increase threshold if many low-value cards remain
        
        # Filter cards that have a value higher than the adjusted bidding threshold
        potential_bids = [card for card in cards if self.get_card_value(card) >= adjusted_threshold]
        
        # If there are potential bids available, choose the highest value card
        if potential_bids:
            return max(potential_bids, key=lambda x: self.get_card_value(x))
        
        # If no potential bids are available, bid the highest card below the adjusted bidding threshold
        return max(cards, key=lambda x: self.get_card_value(x) if self.get_card_value(x) < diamond_value else 0)

    def get_card_value(self, card_name):
        # Define a dictionary to map card names to their numerical values
        card_values = {
            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
            "jack": 11, "queen": 12, "king": 13, "ace": 14
        }
        
        # Extract the numerical value of the card from its name
        if isinstance(card_name, str):
            value_str = card_name.split("_")[0]
            return card_values.get(value_str, 0)
        else:
            return card_name  # Return the integer value directly if it's not a string
