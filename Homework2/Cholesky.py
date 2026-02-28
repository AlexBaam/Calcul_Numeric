import numpy as np
from numpy.linalg import solve


def cholesky(a_matrix, n, epsilon):
    diagonal_array = np.zeros(n, dtype=float)
    for p in range(n):
        d_sum = 0
        for k in range(p):
            d_sum = d_sum + diagonal_array[k] * pow(a_matrix[p,k], 2)
        print("\nd_sum = ", d_sum)

        diagonal_array[p] = a_matrix[p,p] - d_sum
        print("\nDiagonal array is: ", diagonal_array[p])

        if abs(diagonal_array[p]) < epsilon:
            print("Descompunere imposibila fiindca impartim la 0") #Numarul este foarte aproape de 0
            break

        for i in range(p+1, n):
            l_sum = 0
            for k in range(p):
                l_sum = l_sum + diagonal_array[k] * a_matrix[i,k] * a_matrix[p,k]
            print("\nl_sum = ", l_sum)

            a_matrix[i,p] = (a_matrix[i,p] - l_sum)/diagonal_array[p]

            print("\nModified element in a_matrix: ", a_matrix[i,p])

        print("\nFinished an iteration of a step, p increased to: ", p+1)

    return a_matrix, diagonal_array

def cholesky_det(diagonal_array):
    determinant = 1
    for i in range(len(diagonal_array)):
        determinant = determinant * diagonal_array[i]

    return determinant

def cholesky_solve(a_matrix, diagonal_array,n, b_array):
    # L * z = B
    z_unknowns = np.zeros(n)
    y_unknowns = np.zeros(n)
    x_unknowns = np.zeros(n)
    for i in range(n):
        direct_substitution_sum = 0
        for j in range(n):
            if i >= j:
                direct_substitution_sum += a_matrix[i, j] * z_unknowns[j]
                print("\nDirect substitution sum: ", direct_substitution_sum)
        z_unknowns[i] = b_array[i] - direct_substitution_sum
        print(f"\nNecunoscuta Z[{i}]: ", z_unknowns[i])
        print(f"\nGata iteratia {i}")

    # D * y = z
    for i in range(n):
        y_unknowns[i] = z_unknowns[i]/diagonal_array[i]
        print(f"\nNecunoscuta Y[{i}]: ", y_unknowns[i])
        print(f"\nGata iteratia {i}")

    # L.transpose * x = y
    a_matrix = a_matrix.transpose()
    for i in range(n-1, -1, -1):
        inverted_substitution_sum = 0
        for j in range(i+1, n):
            if i <= j:
                inverted_substitution_sum += a_matrix[i, j] * x_unknowns[j]
                print("\nInverted substitution sum: ", inverted_substitution_sum)
        x_unknowns[i] = y_unknowns[i] - inverted_substitution_sum
        print(f"\nNecunoscuta X[{i}]: ", x_unknowns[i])
        print(f"\nGata iteratia {i}")

    a_matrix = a_matrix.transpose()
    return x_unknowns

def multiply_matrix_vector(a_matrix, x_solution, n):
    something_computed = np.zeros(n)
    for i in range(n):
        term_sum = 0
        for j in range(n):
            term_sum += a_matrix[i, j] * x_solution[j]
        print(f"\nTerm on line {i} is: ", term_sum)
        something_computed[i] = term_sum

    print(f"\nComputed multiplication: ", something_computed)
    return something_computed

def run():
    n = 3
    epsilon = 1e-15
    a_matrix = np.array([[4, 2, 2], [2, 5, 1], [2, 1, 3]], dtype=float)

    print("\nMatricea A initiala:")
    print(a_matrix)

    init_a_elements = list()

    for i in range(n):
        for j in range(n):
            if i > j:
                init_a_elements.append(a_matrix[i][j])

    init_a_elements = np.array(init_a_elements, dtype=float)

    print("\nElementele de sub diagonala principala:")
    print(init_a_elements)

    b_array = np.array([8, 13, 9], dtype=float)

    print("\nVector termeni liberi B:")
    print(b_array)

    a_matrix, diagonal_array = cholesky(a_matrix, n, epsilon)

    print("\nMatricea A updatata este:")
    print(a_matrix)

    print("\nVectorul d (Matricea diagonala) este:")
    print(diagonal_array)

    l_elements = list()

    for i in range(n):
        for j in range(n):
            if i > j:
                l_elements.append(a_matrix[i][j])

    l_elements = np.array(l_elements, dtype=float)

    print("\nElementele de sub diagonala principala dupa update:")
    print(l_elements)

    determinant_a_matrix = cholesky_det(diagonal_array)
    print("\nDeterminantul matricei A este: ", determinant_a_matrix)

    system_solution = cholesky_solve(a_matrix, diagonal_array, n, b_array)
    print("\nSolutia sistemului este: ", system_solution)

    k = 0
    for i in range(n):
        for j in range(n):
            if i > j:
                a_matrix[i][j] = init_a_elements[k]
                k += 1

    print("\nMatricea A reconstruita:")
    print(a_matrix)

    a_init_multi_x_chol = multiply_matrix_vector(a_matrix, system_solution, n)

    x_lib = solve(a_matrix, b_array)

    system_norm = np.linalg.norm(a_init_multi_x_chol - b_array)
    solution_euclid_distance = np.linalg.norm(system_solution - x_lib)

    print("\nVerificam norma dintre inmultire si b_array: ", system_norm)
    print("\nVerificam norma dintre solutie gasita de noi si metoda implementata in NumPy: ", solution_euclid_distance)

print(run())
