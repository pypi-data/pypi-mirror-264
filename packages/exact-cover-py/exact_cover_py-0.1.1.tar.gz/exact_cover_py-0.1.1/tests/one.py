#!/usr/bin/env python3

import time

from exact_cover_samples import problems
from exact_cover_py import exact_covers

from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("problem", nargs="?", default="knuth2000", help="problem name")
parser.add_argument("solutions", nargs="?", type=int, default=1, help="how many solutions")
parser.add_argument("runs", nargs="?", type=int, default=1, help="how many runs")
args = parser.parse_args()
P, R, N = args.problem, args.runs, args.solutions


problem = problems[P]()
data = problem["data"]

def main():
    for run in range(R):
        beg = time.time()
        solutions = exact_covers(data)
        try:
            for _ in range(N):
                next(solutions)
        except StopIteration:
            print("no more solutions - skipping")
            pass
        end = time.time()
        print(f"run {run} took {end - beg:.6f} seconds")

main()
