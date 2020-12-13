"""
the rooks and queens problem

positions are encoded as an iterable of Ys in the 0..n-1 range

e.g. (1, 0, 3, 2) is valid (or just as well the same data as a list)
but  (1, 2, 3, 5) is not

later on we use numpy arrays
for drawings and geometric manipulations
and in that context we create nxn square arrays
filled with 0, and one 1 per line - and per column
"""


# the rooks problem is strictly equivalent
# to iterating over Sn, the permutations of [1..n]
def rooks(n):
    """
    generator over the solutions to the rooks problem
    in dimension n

    equivalent to using itertools.permutations of course
    """

    if n == 1 :
        yield [0]
        # we're done here; so we need to end
        # the execution of rooks()
        # (we could also have added a else: clause)
        return

    for smaller in rooks(n-1):
        # assume e.g. n=4
        # we iterate over S3 and for each permutation in S3
        # e.g. smaller=[0, 2, 1]
        # we enumerate in S4 the 4 permutations
        # obtained by inserting <3> in smaller
        # which yields <n> solutions
        # i=0 -> [0, 2, 1, 3]
        # i=1 -> [0, 2, 3, 1]
        # i=2 -> [0, 3, 2, 1]
        # i=3 -> [3, 0, 2, 1]
        for i in range(n):
            # that's why we yield lists and not tuples
            yield smaller[i:] + [n-1] + smaller[:i]


# moving to the queens problem

# check whether a permutation is valid
# notice that one diagonal is defined by an equation like
# x + y = constante
# x - y = constante
# so, for all n points to appear on separate diagonals,
# it is necessary and sufficient that their (x+y) (resp. x-y)
# be all different
# and so, we compute the set of their (x+y) (resp. x-y)
# whose cardinal must be <n>
#
# note on performance; strictly speaking we do not need n
# to be passed to queens_ok, as it is len(L), but having to
# recompute this over and over ad nauseam is a waste of time

def queens_ok(L, n):
    return (
        len({x+y for (x, y) in enumerate(L)}) == n
        and
        len({x-y for (x, y) in enumerate(L)}) == n
    )


def queens(n):
    """
    generator over the solutions to the queens problem
    in dimension n
    """
    # a good example of a closure
    # filter requires a one-argument function
    # so we capture n in a closure, hence the lambda
    return filter(lambda L: queens_ok(L, n), rooks(n))



def generator_size(gen):
    """
    compute the length of an iterator
    as such, it applies to generators too, a fortiori

    WARNING: this will exhaust the input generator
    """
    return sum(map(lambda x: 1, gen))



import numpy as np

def position_to_np(p):
    """
    convert a tuple of numbers between 1 and n
    into a n*n numpy array with ones at the specified locations
    """
    n = len(p)
    a = np.zeros(n*n, dtype=int).reshape((n, n))
    # Ys start at 0
    for x, y in enumerate(p):
        a[x, y] = 1
    return a

def np_to_position(a):
    """
    and the other way around
    we assume the input is mostly zeros,
    with exactly one 1-value per column
    """
    return tuple(np.argmax(a, axis=1))



from matplotlib import pyplot as plt

def draw_position(p):
    """
    position is expected to be a tuple of numbers
    between 1 and n

    create a matplotlib figure
    and draws the position as an imshow()
    """
    a = position_to_np(p)
    plt.figure()
    # use a.T to be compliant with the coordinate system
    # as presented in the README
    plt.imshow(a.T, cmap='inferno')
    plt.yticks(range(len(p)))
    plt.show()



def derived(p):
    """
    enumerates all 8 variants of p after being rotated / symetric

    input p expected to be a position
    """
    a = position_to_np(p)
    for _ in range(4):
        yield np_to_position(a)
        yield np_to_position(a.T)
        a = np.rot90(a)


def uniques(gen):
    """
    our generators yield iterables of Y's

    this generator will eliminate duplicates modulo
    the 8 rotations and symmetries in the 2D space
    """
    # we keep in a set the ones we have already seen
    # together with their 7 reflections / rotations
    known = set()

    for p in gen:
        # we need tuples so we can insert them in a set
        t = tuple(p)
        # already seen ? just skip it
        if t in known:
            continue
        # remember all devived positions in known
        known.update(derived(t))
        yield t
