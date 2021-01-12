# Fichier de test pour la "plomberie"
# Ca ne devrait pas vous intéresser
import unittest

from testing_utils import make_auction


class TestAuction():

    def __init__(self, cli=None):
        self.cli = cli

    def play(self):
        val = self.cli.prompt("give me your name")
        self.cli.display(val)


class TestEcho(unittest.TestCase):

    def test_echo(self):
        cli = make_auction(TestAuction)
        self.assertEqual(['give me your name'], cli.get_displayed())
        cli.type("hello")
        self.assertEqual(['hello'], cli.get_displayed())
        self.assertEqual([], cli.get_displayed())
