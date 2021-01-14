from utils import Cli


class EnglishAuction():

    def __init__(self, cli=None):
        self.cli = cli if cli else Cli()

    def play(self):
        # Input opening bid
        self.cli.display('Started auction of type: English')
        opening_bid = self.cli.prompt('Please enter the opening bid:')
        opening_bid = int(opening_bid)
        self.cli.display(f"Opening bid is: {opening_bid}")

        # Input bidders
        bidders = []
        while True:
            bidder = self.cli.prompt(
                "Enter bidder (enter nothing to move on):"
            )
            if not bidder:
                break
            bidders.append(bidder)
        self.cli.display(f"\nBidders are: {', '.join(bidders)}")

        # Collect bids
        standing_bid = opening_bid
        winner = None
        passed = 0
        last_bidder = None
        while not winner:
            for bidder in bidders:
                bid = self.cli.prompt(
                    f"\nStanding bid is {standing_bid}. {bidder} bids:"
                )
                if bid:
                    bid = int(bid)
                    # bid is expected to be > standing_bid
                    standing_bid = bid
                    passed = 0
                    last_bidder = bidder
                else:
                    passed += 1
                    if passed >= len(bidders)-1:
                        winner = last_bidder
                        break

        # Display winner
        self.cli.display("\n~~~~~~~~\n")
        self.cli.display(f"Winner is {winner}. Winning bid is {standing_bid}.")


if __name__ == "__main__":
    auction = EnglishAuction()
    auction.play()
