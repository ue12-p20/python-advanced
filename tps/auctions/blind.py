from utils import Cli

from auction import Auction

class BlindAuction(Auction):

    type = "Blind"

    def collect_bids(self):
        standing_bid = self.opening_bid
        winner = None
        for bidder in self.bidders:
            bid = self.cli.prompt(
                f"\nOpening bid is {self.opening_bid}. {bidder} bids:"
            )
            bid = int(bid)
            if bid > standing_bid:
                standing_bid = bid
                winner = bidder
        return winner, standing_bid


if __name__ == "__main__":
    auction = BlindAuction()
    auction.play()
