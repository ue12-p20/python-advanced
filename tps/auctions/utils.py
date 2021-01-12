# NE PAS MODIFIER
class Cli():
    def __init__(self):
        self.display = print
        self.input = input

    def display(_, message):
        print(message)

    def prompt(self, message):
        return self.input(message + " ")


if __name__ == "__main__":
    cli = Cli()
    cli.display("testing displays")
    stuff = cli.prompt("enter something")
    print(f"You entered: {stuff}")
