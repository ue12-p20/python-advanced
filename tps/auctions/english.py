from utils import Cli

from auction import Auction

class EnglishAuction(Auction):

    type = "English"

    def collect_bids(self):
        standing_bid = self.opening_bid
        winner = None
        passed = 0
        last_bidder = None
        while not winner:
            for bidder in self.bidders:
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
                    if passed >= len(self.bidders)-1:
                        winner = last_bidder
                        break

        return winner, standing_bid


if __name__ == "__main__":
    auction = EnglishAuction()
    auction.play()
