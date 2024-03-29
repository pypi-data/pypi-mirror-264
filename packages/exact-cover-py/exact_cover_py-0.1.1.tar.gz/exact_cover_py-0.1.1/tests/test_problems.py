from itertools import islice

import pytest

from exact_cover_py import exact_covers

from exact_cover_samples import problems, canonical, canonical_s, canonical_1


def define_test(problem):
    """
    for a given problem defined in problems
    say small_trimino_problem
    we define a derived function named like
    say test_small_trimino_problem
    """

    def test_solutions(problem):
        match problem:
            case {
                "shortname": shortname,
                "name": name,
                "data": data,
                "solutions": solutions,
            }:
                canonical_solutions = canonical(solutions)
                try:
                    canonical_computed = canonical(exact_covers(data))
                    assert canonical_computed == canonical_solutions
                except StopIteration:
                    assert solutions == []

    test_name = f"test_{problem["shortname"]}"
    # if problem_name in PARTIAL_TESTS:
    #     problem["first_solutions"] = PARTIAL_TESTS[problem_name]
    # assign the global variable test_<problem_name>
    # to the newly defined function
    globals()[test_name] = lambda: test_solutions(problem)


for problem_function in problems.values():
    problem = problem_function()
    define_test(problem)
