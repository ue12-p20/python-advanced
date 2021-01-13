import unittest

from vickrey import VickreyAuction
from testing_utils import make_auction


class TestVickrey(unittest.TestCase):
    def test_opening_bid(self):
        cli = make_auction(VickreyAuction)
        self.assertEqual(
            [
                'Started auction of type: Vickrey',
                'Please enter the opening bid:'
            ],
            cli.get_displayed()
        )
        cli.type('30')
        self.assertIn('Opening bid is: 30', cli.get_displayed())

    def test_players(self):
        cli = make_auction(VickreyAuction)
        cli.type('30')
        self.assertIn('Enter bidder (enter nothing to move on):',
                      cli.get_displayed())
        cli.type('alice')
        self.assertEqual(
            ['Enter bidder (enter nothing to move on):'],
            cli.get_displayed()
        )
        cli.type('bob')
        self.assertEqual(
            ['Enter bidder (enter nothing to move on):'],
            cli.get_displayed()
        )
        cli.type('carol')
        self.assertEqual(
            ['Enter bidder (enter nothing to move on):'],
            cli.get_displayed()
        )
        cli.type(None)
        self.assertIn('Bidders are: alice, bob, carol', cli.get_displayed())

    def test_auction(self):
        cli = make_auction(VickreyAuction)
        cli.type('30')
        cli.type('alice')
        cli.type('bob')
        cli.type('carol')
        cli.type(None)
        self.assertIn(
            'Opening bid is 30. alice bids:',
            cli.get_displayed()
        )
        cli.type(35)
        self.assertEqual(
            [
                'Opening bid is 30. bob bids:'
            ],
            cli.get_displayed()
        )
        cli.type(50)
        self.assertEqual(
            [
                'Opening bid is 30. carol bids:'
            ],
            cli.get_displayed()
        )
        cli.type(40)
        self.assertEqual(
            'Winner is carol. Winning bid is 40.',
            cli.get_displayed()[-1]
        )


if __name__ == "__main__":
    unittest.main()
