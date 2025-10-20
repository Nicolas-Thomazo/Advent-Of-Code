"""
--- Day 7: Bridge Repair ---

Link:
    https://adventofcode.com/2024/day/7

"""
#%%
import itertools
from pathlib import Path
from typing import List, Tuple


def remap(sections: str) -> list[tuple[int, list[int]]]:
    """
    Remap example list input provided in "Advent of Code"
    format, to two separate lists.
    """
    equations = sections.strip().split('\n')

    return [(int((res := eq.split(': ', 1))[0]), [int(r) for r in res[1].split(' ')])
            for eq in equations]


def generate_truth_table(n):
    """Generates all possible binary combinations for n variables."""
    return list(itertools.product([0, 1], repeat=n))


def generate_truth_table_for_part_2(n):
    """Generates all possible binary combinations for n variables."""
    return list(itertools.product([0, 1, 2], repeat=n))


def calibration_result_of_true_equations(equations: list[tuple[int, list[int]]]) -> int:
    """
    Solution to Part 1

    *What is their total calibration result?*
    """
    sum_of_test_values = 0

    for test, nums in equations:
        if len(nums) == 1 and nums[0] == test:
            sum_of_test_values += test
            continue

        for operations in generate_truth_table(len(nums) - 1):
            run_total = nums[0]
            for i, op in enumerate(operations, start=1):
                if op == 0:
                    run_total *= nums[i]
                if op == 1:
                    run_total += nums[i]

                # Seems to slow down code, rather than make it faster? Weird.
                # if run_total > test:
                #    break
            else:
                if run_total == test:
                    sum_of_test_values += test
                    break

    return sum_of_test_values


def calibration_result_with_concat_operator(equations: list[tuple[int, list[int]]]) -> int:
    """
    Solution to Part 2

    *What is their total calibration result?*
    """
    sum_of_test_values = 0

    for test, nums in equations:
        if len(nums) == 1 and  nums[0] == test:
            sum_of_test_values += test
            continue

        for operations in generate_truth_table_for_part_2(len(nums) - 1):
            run_total = nums[0]
            for i, op in enumerate(operations, start=1):
                if op == 0:
                    run_total *= nums[i]
                if op == 1:
                    run_total += nums[i]
                if op == 2:
                    run_total = int(f'{run_total}{nums[i]}')

                # Seems to slow down code, rather than make it faster? Weird.
                # if run_total > test:
                #    break
            else:
                if run_total == test:
                    sum_of_test_values += test
                    break

    return sum_of_test_values


def solve(input_file):

    if input_file:
        demo = False
        print(f"Solving with input file {input_file}")
        try:
            INPUT = open(input_file).read()
        except FileNotFoundError:
            print('File not found, using default ...')
            INPUT = open(Path(__file__).parent.parent / 'Inputs' / '07').read()
    else:
        demo = True
        INPUT = DEMO_INPUT

    print("Solving Day 7 Problem! 🎄")

    _equations = remap(INPUT)
    # Part 1
    print('Part 1:  ', calibration_result_of_true_equations(_equations))
    # Part 2
    # print('Part 2:  ', calibration_result_with_concat_operator(_equations))


if __name__ == '__main__':
    solve("test.txt")
# %%
