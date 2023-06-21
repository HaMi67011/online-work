from utils import generate_CSP, generate_assignment, is_consistent
from backtracking import recursive_backtracking
from forwardChecking import forward_checking


def get_unassigned_variable(assignment, CSP):
    minimumDomainSize = 0
    selectedVariable = None

    for variable, assigned_value in assignment.items():
        if len(assigned_value) == 0: # check if the variable has been assigned
            domainSize = len(CSP.get("domains").get(variable))

            # check if the minimum domain size has not been set yet or it is greater than the domain
            if domainSize < minimumDomainSize or minimumDomainSize == 0:
                minimumDomainSize = domainSize
                selectedVariable = variable

    return selectedVariable


def solve(grid_string, multipleSolutions = False):
    CSP = generate_CSP(grid_string)
    assignment = generate_assignment(CSP)
    solutions = []

    recursive_backtracking(assignment, CSP, solutions, multipleSolutions, forward_checking, is_consistent, get_unassigned_variable)

    return solutions, CSP
