from utils import none_inference, is_consistent, get_unassigned_variable, generate_CSP, generate_assignment
from backtracking import recursive_backtracking


def get_domain(variable, CSP):
    domainTuples = []

    # generate the list of the domain values with their frequency of their occurrence in the domain of the neighbors of the variable
    for value in CSP.get("domains").get(variable):
        frequency = 0

        for neightbor in CSP.get("neighbors").get(variable):
            if value in CSP.get("domains").get(neightbor):
                frequency += 1

        domainTuples.append((frequency, value))

    # sort by least frequency to the greatest
    domainTuples.sort(key=lambda x: x[0])

    return [tuple[1] for tuple in domainTuples]


def solve(grid_string, multipleSolutions = False):
    CSP = generate_CSP(grid_string)
    assignment = generate_assignment(CSP)
    solutions = []

    recursive_backtracking(assignment, CSP, solutions, multipleSolutions, none_inference, is_consistent, get_unassigned_variable, get_domain)

    return solutions, CSP
