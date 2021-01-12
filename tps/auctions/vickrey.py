from utils import Cli


class VickreyAuction():
    def __init__(self, cli=None):
        self.cli = cli if cli else Cli()

    def play(self):
        pass


if __name__ == "__main__":
    auction = VickreyAuction()
    auction.play()
