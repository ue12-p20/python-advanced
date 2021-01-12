# NE PAS MODIFIER
import threading
from time import sleep
import sys


class FakeCli():
    SKIP = object()

    def __init__(self):
        self.displayed_messages = []
        self.current_message = None

    def display(self, message):
        self.displayed_messages.append(message)

    def prompt(self, message):
        self.displayed_messages.append(message)
        for _ in range(10):
            if self.current_message is FakeCli.SKIP:
                self.current_message = None
                return
            elif self.current_message:
                typed = self.current_message
                self.current_message = None
                return typed
            sleep(.01)
        raise Exception("No input in the last 100ms")

    def type(self, message):
        for _ in range(10):
            if not self.current_message:
                break
            sleep(.01)
        else:
            raise Exception(
                f"The input \"{self.current_message}\" wasn't consumed in the last 100ms"
            )

        self.current_message = message if message else FakeCli.SKIP

    def get_displayed(self):
        sleep(.02)
        for _ in range(10):
            if self.displayed_messages:
                messages = self.displayed_messages
                self.displayed_messages = []
                return [m.strip() for m in messages]
            sleep(.1)
        return []


def make_auction(auction_cls):
    cli = FakeCli()
    auction = auction_cls(cli)

    def wrapped_play():
        try:
            auction.play()
        except Exception as e:
            pass
            # sys.stderr.write(str(e))
            # sys.stderr.flush()

    t = threading.Thread(target=wrapped_play, daemon=True)
    t.start()
    return cli


if __name__ == "__main__":
    class EchoAuction():
        def __init__(self, cli):
            self.cli = cli

        def play(self):
            self.cli.display("testing displays")
            stuff = self.cli.prompt("enter stuff")
            self.cli.display(f"you entered: {stuff}")

    cli = make_auction(EchoAuction)
    print(cli.get_displayed())
    cli.type('something')
    print(cli.get_displayed())
