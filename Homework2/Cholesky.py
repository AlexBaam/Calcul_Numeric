import numpy as np
from numpy.linalg import solve

'''
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

# print(run_random())
print(run())
'''

def cholesky(a_matrix, n, epsilon, large_matrix):
    diagonal_array = np.zeros(n, dtype=float)

    for p in range(n):
        d_sum = 0
        for k in range(p):
            d_sum = d_sum + diagonal_array[k] * (a_matrix[p,k] * a_matrix[p,k]) # Renuntam la pow fiindca e mai eficient sa facem inmultiri

        if not large_matrix:
            print("\nd_sum = ", d_sum)

        diagonal_array[p] = a_matrix[p,p] - d_sum
        if not large_matrix:
            print("\nDiagonal array element is: ", diagonal_array[p])

        if abs(diagonal_array[p]) < epsilon:
            print(f"\nDescompunere imposibila la pasul p={p} fiindca impartim la 0") #Numarul este foarte aproape de 0
            break

        for i in range(p+1, n):
            l_sum = 0
            for k in range(p):
                l_sum = l_sum + diagonal_array[k] * a_matrix[i,k] * a_matrix[p,k]

            if not large_matrix:
                print("\nl_sum = ", l_sum)

            a_matrix[i,p] = (a_matrix[i,p] - l_sum)/diagonal_array[p]

            if not large_matrix:
                print("\nModified element in a_matrix: ", a_matrix[i,p])

        if not large_matrix:
            print("\nFinished an iteration of a step, p increased to: ", p+1)

    if large_matrix:
        print("Finished computing the Cholesky decomposition")
    return a_matrix, diagonal_array

def cholesky_det(diagonal_array, large_matrix):

    if large_matrix:
        return float("inf")

    determinant = 1
    for i in range(len(diagonal_array)):
        determinant = determinant * diagonal_array[i]

    return determinant

def cholesky_solve(a_matrix, diagonal_array,n, b_array, large_matrix):
    # L * z = B
    z_unknowns = np.zeros(n)
    y_unknowns = np.zeros(n)
    x_unknowns = np.zeros(n)
    for i in range(n):
        direct_substitution_sum = 0
        for j in range(i):
            if i >= j:
                direct_substitution_sum += a_matrix[i, j] * z_unknowns[j]
                if not large_matrix:
                    print("\nDirect substitution sum: ", direct_substitution_sum)
        z_unknowns[i] = b_array[i] - direct_substitution_sum
        if not large_matrix:
            print(f"\nNecunoscuta Z[{i}]: ", z_unknowns[i])
            print(f"\nGata iteratia {i}")

    # D * y = z
    for i in range(n):
        y_unknowns[i] = z_unknowns[i]/diagonal_array[i]
        if not large_matrix:
            print(f"\nNecunoscuta Y[{i}]: ", y_unknowns[i])
            print(f"\nGata iteratia {i}")

    # L.transpose * x = y
    a_matrix = a_matrix.transpose()
    for i in range(n-1, -1, -1):
        inverted_substitution_sum = 0
        for j in range(i+1, n):
            if i <= j:
                inverted_substitution_sum += a_matrix[i, j] * x_unknowns[j]
                if not large_matrix:
                    print("\nInverted substitution sum: ", inverted_substitution_sum)
        x_unknowns[i] = y_unknowns[i] - inverted_substitution_sum
        if not large_matrix:
            print(f"\nNecunoscuta X[{i}]: ", x_unknowns[i])
            print(f"\nGata iteratia {i}")

    a_matrix = a_matrix.transpose()
    return x_unknowns

def multiply_matrix_vector(a_matrix, x_solution, n, large_matrix):
    something_computed = np.zeros(n)
    for i in range(n):
        term_sum = 0
        for j in range(n):
            term_sum += a_matrix[i, j] * x_solution[j]
        if not large_matrix:
            print(f"\nTerm on line {i} is: ", term_sum)
        something_computed[i] = term_sum

    print(f"\nComputed multiplication: ", something_computed)
    return something_computed

def gen_random_matrix(n):

    large_matrix = n > 100

    b_matrix = np.random.randn(n, n)
    a_matrix = b_matrix @ b_matrix.T

    b_array = np.random.randn(n)

    if not large_matrix:
        print("Matricea B:")
        print(b_matrix)
        print("\nMatricea A:")
        print(a_matrix)

    return a_matrix, b_array

def run():
    '''
    n = 3
    epsilon = 1e-15
    a_matrix = np.array([[4, 2, 2], [2, 5, 1], [2, 1, 3]], dtype=float)
    b_array = np.array([8, 13, 9], dtype=float)
    '''

    n = 1000
    epsilon = 1e-15
    a_matrix, b_array = gen_random_matrix(n)

    large_matrix = n > 100

    if not large_matrix:
        print("\nMatricea A initiala:")
        print(a_matrix)

    if not large_matrix:
        print("\nVector termeni liberi B:")
        print(b_array)

    init_a_elements = list()

    for i in range(n):
        for j in range(n):
            if i > j:
                init_a_elements.append(a_matrix[i][j])

    init_a_elements = np.array(init_a_elements, dtype=float)

    if not large_matrix:
        print("\nElementele de sub diagonala principala:")
        print(init_a_elements)

    a_matrix, diagonal_array = cholesky(a_matrix, n, epsilon, large_matrix)

    if not large_matrix:
        print("\nMatricea A updatata este:")
        print(a_matrix)

    if not large_matrix:
        print("\nVectorul d (Matricea diagonala) este:")
        print(diagonal_array)

    l_elements = list()

    for i in range(n):
        for j in range(n):
            if i > j:
                l_elements.append(a_matrix[i][j])

    l_elements = np.array(l_elements, dtype=float)

    if not large_matrix:
        print("\nElementele de sub diagonala principala dupa update:")
        print(l_elements)

    determinant_a_matrix = cholesky_det(diagonal_array, large_matrix)
    print("\nDeterminantul matricei A este: ", determinant_a_matrix)

    system_solution = cholesky_solve(a_matrix, diagonal_array, n, b_array, large_matrix)
    print("\nSolutia sistemului este: ", system_solution)

    k = 0
    for i in range(n):
        for j in range(n):
            if i > j:
                a_matrix[i][j] = init_a_elements[k]
                k += 1

    if not large_matrix:
        print("\nMatricea A reconstruita:")
        print(a_matrix)

    a_init_multi_x_chol = multiply_matrix_vector(a_matrix, system_solution, n, large_matrix)

    x_lib = solve(a_matrix, b_array)

    system_norm = np.linalg.norm(a_init_multi_x_chol - b_array)
    solution_euclid_distance = np.linalg.norm(system_solution - x_lib)

    print("\nVerificam norma dintre inmultire si b_array: ", system_norm)
    print("\nVerificam norma dintre solutie gasita de noi si metoda implementata in NumPy: ", solution_euclid_distance)

print(run())
