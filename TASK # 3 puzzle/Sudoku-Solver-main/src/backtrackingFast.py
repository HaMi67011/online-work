from utils import get_neighbors, parse_sudoku_grid_string, grid_index_to_row_and_col, is_valid_assignment
from backtracking import recursive_backtracking


def generate_CSP(sudoku_grid_string):
    '''
    variables: cells 0 to 80
    domain: 1 to 9
    constraints:
        no integer is allowed to appear twice in any row or column
        no integer is allowed to appear twice in NxN subgrids that constructs the boards

        this is implemented in:
            is_valid_assignment()
    '''

    N = 9 * 9 # number of cells

    # create the variable list
    variables = [col for col in range(N)]

    # create the domain for each variable in variables list
    domains = {var: [pos for pos in range(1, 10)] for var in variables}

    # find the neighbors for each variable
    neighbors = {var: get_neighbors(var) for var in variables}

    # create a CSP dictionary
    csp = {
        "variables": variables,
        "domains": domains,
        "neighbors": neighbors
    }

    grid = parse_sudoku_grid_string(sudoku_grid_string)

    for i in range(81):
        row, col = grid_index_to_row_and_col(i)

        given_value = grid[row][col]

        if given_value > 0 and given_value < 10:
            grid[row][col] = 0

            if is_valid_assignment(grid, given_value, i):
                csp.get("domains")[i] = [given_value]
            else:
                # clear all domains
                csp["domains"] = {var: [] for var in variables}
                break

            grid[row][col] = given_value

    return csp


def generate_assignment(CSP):
    # create a dictionary with the values as empty lists
    assignment = {var: [] for var in CSP.get("variables")}

    # assigned given values to the variables
    for i in range(81):
        domain = CSP.get("domains").get(i)

        if len(domain) == 1:
            assignment.get(i).append(domain[0])

    return assignment


def solve(grid_string, multipleSolutions = False):
    CSP = generate_CSP(grid_string)
    assignment = generate_assignment(CSP)
    solutions = []

    recursive_backtracking(assignment, CSP, solutions, multipleSolutions)

    return solutions, CSP
