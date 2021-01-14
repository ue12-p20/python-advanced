from utils import Cli

class Auction:

    def __init__(self, cli=None):
        self.cli = cli if cli else Cli()
        self.opening_bid = 0
        self.bidders = []

    def input_bidders(self):
        # Input bidders
        self.bidders = []
        while True:
            bidder = self.cli.prompt(
                "Enter bidder (enter nothing to move on):"
            )
            if not bidder:
                break
            self.bidders.append(bidder)
        display = ', '.join(self.bidders)
        self.cli.display(f"\nBidders are: {display}")

    def input_opening_bid(self):
        # Input opening bid
        self.cli.display(f'Started auction of type: {self.type}')
        opening_bid = self.cli.prompt('Please enter the opening bid:')
        self.opening_bid = int(opening_bid)
        self.cli.display(f"Opening bid is: {self.opening_bid}")

    def play(self):
        self.input_opening_bid()
        self.input_bidders()
        winner, bid = self.collect_bids()
        self.display_winner(winner, bid)


    def display_winner(self, winner, standing_bid):
        # Display winner
        self.cli.display("\n~~~~~~~~\n")
        self.cli.display(f"Winner is {winner}. Winning bid is {standing_bid}.")
