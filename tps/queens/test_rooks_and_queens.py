from math import factorial
from rooks_and_queens import rooks, queens

def iter_len(x):
    return sum(map(lambda _: 1, x))

queens_sizes = [
    (2, 0),
    (3, 0),
    (4, 2),
    (5, 10),
    (6, 4),
    (7, 40),
    (8, 92),
    (9, 352),
    (10, 724),
]

unique_queens_sizes = [
    (2, 0),
    (3, 0),
    (4, 1),
    (5, 2),
    (6, 1),
    (7, 6),
    (8, 12),
    (9, 46),
    (10, 92),
]

def test_rooks():
    for (n, _) in queens_sizes:
        assert iter_len(rooks(n)) == factorial(n)

def test_queens():
    for (n, size) in queens_sizes:
        assert iter_len(queens(n)) == size

try:
    from rooks_and_queens import uniques
    def test_unique_queens():
        for (n, size) in unique_queens_sizes:
            assert iter_len(uniques(queens(n))) == size
except:
    print(f"uniques not found - skipping")
