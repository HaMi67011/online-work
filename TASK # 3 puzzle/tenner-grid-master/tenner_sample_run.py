from tenner_csp import *
from propagators import *
import ast, sys

b1 = ([[-1, 6, 2, 0,-1,-1,-1, 8, 5, 7],
       [-1, 0, 1, 7, 8,-1,-1,-1, 9,-1],
       [-1, 4,-1,-1, 2,-1, 3, 7,-1, 8]],
       [13,10, 8, 7,19,16,11,19,15,17])

b2 = ([[-1,-1, 1,-1, 3, 8, 6, 9,-1, 2],
       [ 6, 2,-1,-1, 1,-1,-1, 7, 4, 3],
       [ 7, 4, 5,-1, 0, 6,-1,-1, 8,-1],
       [-1,-1, 8,-1, 4, 9, 5, 7,-1,-1],
       [ 7, 9, 1, 0,-1,-1, 4, 8, 5, 2],],
       [26,20,15,27,14,35,21,34,23,10])

def print_tenner_soln(var_array):
    for row in var_array:
        print([var.get_assigned_value() for var in row])

if __name__ == "__main__":

    for b in [b1, b2]:
        print("Solving board:")
        for row in b[0]:
            print(row)

        print("Using Model 1")
        csp, var_array = tenner_csp_model_1(b)
        solver = BT(csp)
        print("=======================================================")
        print("FC")
        solver.bt_search(prop_FC)
        print("Solution")
        print_tenner_soln(var_array)
        
        print("Using Model 2")
        csp, var_array = tenner_csp_model_2(b)
        solver = BT(csp)
        print("=======================================================")
        print("GAC")
        solver.bt_search(prop_GAC)
        print("Solution")
        print_tenner_soln(var_array)

