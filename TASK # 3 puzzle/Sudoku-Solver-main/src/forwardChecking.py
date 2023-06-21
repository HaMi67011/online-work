from utils import generate_CSP, generate_assignment
from backtracking import recursive_backtracking
import copy


def forward_checking(CSP, variable, assignment):
    # copy the dictionary to avoid pointing to the same dictionary
    new_CSP = copy.deepcopy(CSP)

    for neighbor in new_CSP.get("neighbors").get(variable):
        if assignment.get(variable)[0] in new_CSP.get("domains").get(neighbor):
            new_CSP.get("domains").get(neighbor).remove(assignment.get(variable)[0])

            if len(new_CSP.get("domains").get(neighbor)) == 0:
                return False, new_CSP

    return True, new_CSP


def solve(grid_string, multipleSolutions = False):
    CSP = generate_CSP(grid_string)
    assignment = generate_assignment(CSP)
    solutions = []

    recursive_backtracking(assignment, CSP, solutions, multipleSolutions, forward_checking)

    return solutions, CSP
