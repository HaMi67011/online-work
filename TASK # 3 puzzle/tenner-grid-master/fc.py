def select_unassigned_variable(variables, assignment):
    unassigned_vars = [var for var in variables if var not in assignment]
    return unassigned_vars[0]  # Select the first unassigned variable

def is_assignment_complete(assignment, variables):
    return len(assignment) == len(variables)

def is_consistent(variable, value, assignment, constraints, domains):
    for constraint in constraints[variable]:
        if constraint[0] in assignment:
            if assignment[constraint[0]] == value:
                return False
        else:
            if not has_valid_assignment(constraint[0], value, assignment, constraints, domains):
                return False
    return True

def has_valid_assignment(variable, value, assignment, constraints, domains):
    for val in domains[variable]:
        if is_consistent(variable, val, assignment, constraints, domains):
            return True
    return False

def forward_checking(variables, domain, constraints):
    assignment = {}
    domains = domain.copy()
    return backtrack(assignment, variables, domains, constraints)

def backtrack(assignment, variables, domains, constraints):
    if is_assignment_complete(assignment, variables):
        return assignment

    var = select_unassigned_variable(variables, assignment)
    for value in domains[var]:
        if is_consistent(var, value, assignment, constraints, domains):
            assignment[var] = value

            updated_domains = domains.copy()
            for neighbor in constraints[var]:
                if neighbor[0] not in assignment:
                    updated_domains[neighbor[0]] = [val for val in updated_domains[neighbor[0]] if val != value]

            result = backtrack(assignment, variables, updated_domains, constraints)
            if result is not None:
                return result

            del assignment[var]
    return None
