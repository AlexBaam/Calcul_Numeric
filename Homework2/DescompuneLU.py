import pprint
import numpy as np
import scipy.linalg
from numpy.linalg import solve

def desc_lu(a_matrix):
    permutation_matrix, lower_triangular, upper_triangular = scipy.linalg.lu(a_matrix)

    print("\nL:")
    pprint.pprint(lower_triangular)

    print("\nU:")
    pprint.pprint(upper_triangular)

    return lower_triangular, upper_triangular

def run_random():
    n = 3
    b_matrix = np.random.randn(n, n)
    a_matrix = b_matrix @ b_matrix.T

    print("Matricea B:")
    print(b_matrix)
    print("\nMatricea A:")
    print(a_matrix)

    desc_lu(a_matrix)

def run():
    a_matrix = np.array([[4, 2, 2], [2, 5, 1], [2, 1, 3]])

    print("\nMatricea A:")
    print(a_matrix)

    b_array = np.array([8, 13, 9])

    print("\nVector termeni liberi B:")
    print(b_array)

    x_lib = solve(a_matrix, b_array)

    print("\nSolutie:")
    print("\n",x_lib)

print(run())