# pylint: disable=invalid-name

"""
Donald Knuth's Algorithm X implemented in Python

references point to taocp - chapter 7.2.2.1
in Volume 4B
"""

import numpy as np

import numba as nb

# DTYPE = np.int16
# UNUSED = -(2**15)
DTYPE = np.int64
UNUSED = -(2**63)


@nb.njit
def init(problem: np.ndarray):
    """
    problem is expected to be a boolean matrix
    representing the exact cover problem

    see:
     (10) p.3 and
      Table 1. p. 4
    """
    N, M = problem.shape
    nb_nodes = problem.sum()
    # adding the root node and spacer nodes in the mix
    Z = 1 + M + nb_nodes + N + 1
    LLINK = np.zeros(M+1, dtype=DTYPE)
    RLINK = np.zeros(M+1, dtype=DTYPE)

    TOP = np.zeros(Z, dtype=DTYPE)
    ULINK = np.zeros(Z, dtype=DTYPE)
    DLINK = np.zeros(Z, dtype=DTYPE)

    LLINK[:] = (np.arange(M+1) - 1) % (M+1)
    RLINK[:] = (np.arange(M+1) + 1) % (M+1)

    # labelled LEN in the original paper
    TOP[0] = ULINK[0] = DLINK[0] = UNUSED
    TOP[1:M+1] = np.sum(problem, axis=0)

    # fill ULINK and TOP
    previous = np.arange(M) + 1
    counter = M+1
    # first spacer node
    ULINK[counter] = UNUSED
    for i in range(N):
        row = problem[i]
        first_in_row = 0
        for j, b in enumerate(row):
            if b:
                counter += 1
                ULINK[counter] = previous[j]
                TOP[counter] = j+1
                previous[j] = counter
                if first_in_row == 0:
                    first_in_row = counter
        # spacer node
        counter += 1
        ULINK[counter] = first_in_row
        TOP[counter] = -(i+1)
    # we can now fill the first row
    ULINK[1:M+1] = previous

    # fill DLINK - counter already OK but let's be safe
    previous = np.arange(M) + 1
    counter = Z-1
    DLINK[counter] = UNUSED
    for i in range(N-1, -1, -1):
        row = problem[i]
        last_in_row = 0
        for j in range(M-1, -1, -1):
            b = row[j]
            if b:
                counter -= 1
                DLINK[counter] = previous[j]
                previous[j] = counter
                if last_in_row == 0:
                    last_in_row = counter
        # spacer node
        counter -= 1
        DLINK[counter] = last_in_row
    # we can now fill the first row
    DLINK[1:M+1] = previous

    return LLINK, RLINK, TOP, ULINK, DLINK


@nb.njit("void(i8, i8[:], i8[:], i8[:], i8[:], i8[:])", cache=True)
def hide(p, LLINK, RLINK, TOP, ULINK, DLINK):
    """
    (13) p. 5
    """
    q = p + 1
    while q != p:
        x, u, d = TOP[q], ULINK[q], DLINK[q]
        if x <= 0:
            # spacer
            q = u
        else:
            DLINK[u], ULINK[d] = d, u
            TOP[x] -= 1
            q += 1


@nb.njit("void(i8, i8[:], i8[:], i8[:], i8[:], i8[:])", cache=True)
def cover(i, LLINK, RLINK, TOP, ULINK, DLINK):
    """
    (12) p. 4
    """
    p = DLINK[i]
    while p != i:
        hide(p, LLINK, RLINK, TOP, ULINK, DLINK)
        p = DLINK[p]

    l, r = LLINK[i], RLINK[i]
    RLINK[l], LLINK[r] = r, l


@nb.njit("void(i8, i8[:], i8[:], i8[:], i8[:], i8[:])", cache=True)
def unhide(p, LLINK, RLINK, TOP, ULINK, DLINK):
    """
    (15) p. 5
    """
    q = p - 1
    while q != p:
        x, u, d = TOP[q], ULINK[q], DLINK[q]
        if x <= 0:
            # spacer
            q = d
        else:
            DLINK[u], ULINK[d] = q, q
            TOP[x] += 1
            q -= 1


@nb.njit("void(i8, i8[:], i8[:], i8[:], i8[:], i8[:])", cache=True)
def uncover(i, LLINK, RLINK, TOP, ULINK, DLINK):
    """
    (14) p. 5
    """
    l, r = LLINK[i], RLINK[i]
    RLINK[l], LLINK[r] = i, i
    p = ULINK[i]
    while p != i:
        unhide(p, LLINK, RLINK, TOP, ULINK, DLINK)
        p = ULINK[p]


@nb.njit("i8(i8, i8[:])", cache=True)
def spot_solution(x, TOP):
    """
    (16) p. 5
    """
    while TOP[x] >= 0:
        x += 1
    return -TOP[x] - 1


@nb.njit("(i8[:], i8[:], i8[:], i8[:], i8[:])",
         cache=True,
         )
def algorithm_x(LLINK, RLINK, TOP, ULINK, DLINK):
    """
    p. 5
    """

    # X1 - done in init beeforehand
    N = len(LLINK) - 1
    Z = len(DLINK) - 1

    X = np.zeros(N+1, dtype=DTYPE)
    depth = 0       # X1    # is called l in the book

    step = 2
    # i = None - would crash numba
    while True:
        if step == 2:                   # X2
            if RLINK[0] == 0:
                yield [spot_solution(x, TOP) for x in X[:depth]]
                step = 8
            else:
                step = 3
        elif step == 3:                 # X3
            # spot i so that TOP[i] is minimal
            smallest = TOP[RLINK[0]]
            i = nav = RLINK[0]
            while nav != 0:
                if TOP[nav] < smallest:
                    smallest = TOP[nav]
                    i = nav
                nav = RLINK[nav]
            step = 4
        elif step == 4:                 # X4
            cover(i, LLINK, RLINK, TOP, ULINK, DLINK)
            X[depth] = DLINK[i]
            step = 5
        elif step == 5:                 # X5
            if X[depth] == i:
                step = 7
            else:
                p = X[depth] + 1
                while p != X[depth]:
                    j = TOP[p]
                    if j <= 0: # spacer
                        p = ULINK[p]
                    else:
                        cover(j, LLINK, RLINK, TOP, ULINK, DLINK)
                        p += 1
                depth += 1
                step = 2
        elif step == 6:                 # X6
            p = X[depth] - 1
            while p != X[depth]:
                j = TOP[p]
                if j <= 0:
                    p = DLINK[p]
                else:
                    uncover(j, LLINK, RLINK, TOP, ULINK, DLINK)
                    p -= 1
            i = TOP[X[depth]]
            X[depth] = DLINK[X[depth]]
            step = 5
        elif step == 7:                 # X7
            uncover(i, LLINK, RLINK, TOP, ULINK, DLINK)
            step = 8
        elif step == 8:                 # X8
            if depth == 0:
                return
            else:
                depth -= 1
                step = 6


def exact_covers(array: np.ndarray):
    """
    a generator that yields all solutions
    """
    LLINK, RLINK, TOP, ULINK, DLINK = init(array)
    yield from algorithm_x(LLINK, RLINK, TOP, ULINK, DLINK)


def sanity_check(array: np.ndarray):
    """
    checks that the input array is a valid exact cover problem
    """
    if array.ndim != 2:
        raise ValueError("input should be 2-dimensional")
    if not np.all(array == array.astype(bool)):
        raise ValueError("input should be boolean only")
