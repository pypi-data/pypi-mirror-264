#!/usr/bin/env python3

import time
from itertools import count

from exact_cover_samples import problems
from exact_cover_py import exact_covers

from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("-s", "--size", type=int, default=1, help="how many solutions")
parser.add_argument("-r", "--runs", type=int, default=1, help="how many runs")
parser.add_argument("problem", nargs="?", default="p3x20", help="problem name")
parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
args = parser.parse_args()
P, runs, size = args.problem, args.runs, args.size


problem = problems[P]()
data = problem["data"]

def main():
    for run in range(runs):
        beg = time.time()
        solutions = exact_covers(data)
        iterator = count() if size == 0 else range(size)
        try:
            for _ in iterator:
                s = next(solutions)
                if args.verbose:
                    print(s)
        except StopIteration:
            expected = "all" if size == 0 else size
            print(f"asked for {expected} solutions, and found {_}")
            pass
        end = time.time()
        print(f"run {run} took {end - beg:.6f} seconds")

main()
