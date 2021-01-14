from utils import Cli

from auction import Auction

class VickreyAuction(Auction):

    type = "Vickrey"

    def collect_bids(self):
        bids = []
        for bidder in self.bidders:
            bids.append(
                (bidder,
                 self.cli.prompt(
                 f"\nOpening bid is {self.opening_bid}. {bidder} bids:"
            )))
        bids.sort(key=lambda t: t[1])
        return bids[-1][0], bids[-2][1]


if __name__ == "__main__":
    auction = VickreyAuction()
    auction.play()
