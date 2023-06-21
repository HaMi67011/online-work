def grid_index_to_row_and_col(index):
    row = index // 9
    col = index % 9

    return row, col


def get_neighbors(cell_id):
    row, column = grid_index_to_row_and_col(cell_id)

    neighbors = set()

    # get row
    for i in range(9):
        neighbors.add(9 * row + i)

    # get column
    for i in range(9):
        neighbors.add(i * 9 + column)

    # get subgrid
    start_row = row - (row % 3)
    start_column = column - (column % 3)
    for i in range(3):
        for j in range(3):
            neighbors.add((i + start_row) * 9 + (j + start_column))

    neighbors.remove(cell_id)

    return list(neighbors)


def parse_sudoku_grid_string(sudoku_grid_string):
    """
    parse sudoku string
    """
    rows = sudoku_grid_string.strip().split("\n")
    return [[int(num) for num in row.split()] for row in rows]


def is_valid_assignment(grid, number, index):
    row, column = grid_index_to_row_and_col(index)

    # check row
    for i in range(9):
        if grid[row][i] == number:
            return False
 
    # check column
    for i in range(9):
        if grid[i][column] == number:
            return False
 
    # check subgrid
    start_row = row - (row % 3)
    start_column = column - (column % 3)
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_column] == number:
                return False

    return True


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

        if given_value != 0:
            csp.get("domains")[i] = [given_value]

    return csp


def generate_assignment(CSP):
    # create a dictionary with the values as empty lists
    assignment = {var: [] for var in CSP.get("variables")}

    return assignment


def generate_sudoku_string(assignment, CSP):
    """
    generate a string for the sudoku grid
    """

    grid = ""

    for cell in CSP.get("variables"):
        grid += str(assignment.get(cell)[0])

        if (cell + 1) % 9 == 0:
            if cell != 0 and cell != 80:
                grid += "\n"
        else:
            grid += " "

    return grid


def convert_assignment_to_grid(assignment, CSP):
    """
    make a grid (2d array) from the assignment object
    """

    grid = [[0 for _ in range(9)] for _ in range(9)] 

    for i in range(81):
        given_assignment = CSP.get("domains").get(i)

        if len(given_assignment) == 1:
            row, col = grid_index_to_row_and_col(i)
            grid[row][col] = given_assignment[0]

    for key, dict_value in assignment.items():
        row, col = grid_index_to_row_and_col(key)

        if len(dict_value) != 0:
            grid[row][col] = dict_value[0]

    return grid


def is_consistent(value, variable, assignment, CSP):
    for neightbor in CSP.get("neighbors").get(variable):
        if value in assignment.get(neightbor):
            return False

    return True


def is_assignment_complete(assignment):
    """
    check if the assignment is complete.

    the assignment is complete when all the variables have an assignment
    """

    for key, value in assignment.items():
        if len(value) == 0: # check if the variable has been assigned
            return False
    return True


def get_unassigned_variable(assignment, CSP):
    """
    return a variable that has not been assigned yet

    ex: assignment = {
            0: [1],
            1: [],
            2: [4]
        }

        returns variable 1
    """
    for variable, assigned_value in assignment.items():
        if len(assigned_value) == 0: # check if the variable has been assigned
            return variable


def none_inference(CSP, variable, assignment):
    return True, CSP


def get_domain(variable, CSP):
    return CSP.get("domains").get(variable)
