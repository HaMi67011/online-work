# from backtracking import solve as back_solve
from backtrackingFast import solve as back_fast_solve
from forwardChecking import solve as forward_solve
from arcConsistency import solve as arc_solve
from minimumRemainingValue import solve as mrv_solve
from leastConstrainingValue import solve as lcv_solve
from combinedMethods import solve as combined_solve
from utils import generate_sudoku_string


def printSolutions(solutions, CSP):
    if len(solutions) == 0:
        print("No solution found\n")
    else:
        for solution in solutions:
            print(generate_sudoku_string(solution, CSP))
            print()


def main():
    '''
    Each value is separated by a space
    A zero means an empty cell on the sudoku grid
    '''
    grid_string = """
    5 3 0 0 7 0 0 0 0
    6 0 0 1 9 5 0 0 0
    0 9 8 0 0 0 0 6 0
    8 0 0 0 6 0 0 0 3
    4 0 0 8 0 3 0 0 1
    7 0 0 0 2 0 0 0 6
    0 6 0 0 0 0 2 8 0
    0 0 0 4 1 9 0 0 5
    0 0 0 0 8 0 0 7 9
    """

    # show single solution

    print("single solutions\n")

    # very slow
    # print("backtracking\n")
    # printSolutions(*back_solve(grid_string))

    print("backtracking fast\n")
    printSolutions(*back_fast_solve(grid_string))

    print("forward checking\n")
    printSolutions(*forward_solve(grid_string))

    print("arc consistency\n")
    printSolutions(*arc_solve(grid_string))

    print("minimum remaining value\n")
    printSolutions(*mrv_solve(grid_string))

    print("least constraining value\n")
    printSolutions(*lcv_solve(grid_string))

    print("combined methods\n")
    printSolutions(*combined_solve(grid_string))


    # show multiple solutions

    print("\nmultiple solutions\n")

    # very slow
    # print("-------------------------\nbacktracking\n")
    # printSolutions(*back_solve(grid_string, True))

    print("-------------------------\nbacktracking fast\n")

    printSolutions(*back_fast_solve(grid_string, True))

    print("-------------------------\nforward checking\n")

    printSolutions(*forward_solve(grid_string, True))

    print("-------------------------\narc consistency\n")

    printSolutions(*arc_solve(grid_string, True))

    print("-------------------------\nminimum remaining value\n")
    printSolutions(*mrv_solve(grid_string, True))

    print("-------------------------\nleast constraining value\n")
    printSolutions(*lcv_solve(grid_string, True))

    print("-------------------------\ncombined methods\n")
    printSolutions(*combined_solve(grid_string, True))


if __name__ == "__main__":
    main()
