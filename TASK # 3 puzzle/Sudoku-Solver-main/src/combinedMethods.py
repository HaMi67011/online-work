from utils import is_consistent
from backtracking import recursive_backtracking
from backtrackingFast import solve as generate_CSP, generate_assignment
from forwardChecking import forward_checking
from arcConsistency import arc_consistency
from minimumRemainingValue import get_unassigned_variable
from leastConstrainingValue import get_domain


def solve(grid_string, multipleSolutions = False):
    CSP = generate_CSP(grid_string)
    assignment = generate_assignment(CSP)
    solutions = []

    is_arc_consistent, new_csp = arc_consistency(CSP)

    if (is_arc_consistent):
        recursive_backtracking(assignment, new_csp, solutions, multipleSolutions, forward_checking, is_consistent, get_unassigned_variable, get_domain)

    return solutions, new_csp
