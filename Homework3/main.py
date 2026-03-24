import math
import time

import numpy as np

def calcul_vector_b(A, s, afisare):
    n = len(s)
    b = np.zeros(n, dtype=float)
    if afisare:
        for i in range(n):
            for j in range(n):
                b[i] += A[i][j] * s[j]
    else:
        A = np.array(A, dtype=float)
        s = np.array(s, dtype=float)
        return A @ s
    return b

def descompunere_householder_qr(A, n, b, epsilon, afisare):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    R = np.copy(A)
    Q = np.eye(n, dtype=float) # matricea identitate
    if afisare:
        print(f"Matricea R initiala:\n {R}\n")
        print(f"Matricea Q initiala:\n {Q}\n")

    for r in range(n-1):
        if afisare:
            print(f"\nPasul r = {r}\n")

        # suma patratelor elementelor de pe coloana r, de la linia r in jos
        sigma = 0
        for i in range(r, n):
            sigma += R[i][r] ** 2

            if afisare:
                print("sigma = ", sigma)

        # verificare daca coloana r e aproape nula
        if sigma <= epsilon:
            print(f"Coloana {r} este aproape 0. Matricea este singulara. Ne oprim.")
            break

        k = np.sqrt(sigma)
        if R[r][r] > 0:
            k = -k

        if afisare:
            print("k = ", k)

        # constanta reflectprului
        beta = sigma - k * R[r][r]
        if afisare:
            print("beta = ", beta)

        u = np.zeros(n, dtype=float)
        u[r] = R[r][r] - k
        for i in range(r+1, n):
            u[i] = R[i][r]

        if afisare:
            print("\nVectorul u:\n", u)

        # transformarea coloanelor j = r+1,...,n-1 / adica toate coloanele din dreapta coloanei r
        for j in range(r+1,n):
            suma_gamma = 0
            for i in range(r,n):
                suma_gamma += u[i] * R[i][j]
            gamma = suma_gamma / beta

            for i in range(r, n):
                R[i][j] = R[i][j] - gamma * u[i]

        if afisare:
            print("\nR dupa transformarea coloanelor:", R)

        # transformarea coloanei r
        R[r, r] = k
        for i in range(r+1,n):
            R[i][r] = 0

        if afisare:
            print("\nR dupa ce am pus 0 sub diagonala:", R)

        # transformarea lui b
        suma_gamma = 0
        for i in range(r, n):
            suma_gamma += u[i] * b[i]
        gamma = suma_gamma / beta

        for i in range(r, n):
            b[i] = b[i] - gamma * u[i]

        if afisare:
            print("\nb dupa transformare:", b)

        # actualizarea lui Q
        for j in range(n):
            suma_gamma = 0
            for i in range(r, n):
                suma_gamma += u[i] * Q[i][j]
            gama = suma_gamma / beta

            for i in range(r, n):
                Q[i][j] = Q[i][j] - gama * u[i]

    print(f"\nMatricea Q:\n {Q.T}")
    print(f"\nMatricea R:\n {R}\n")
    return Q.T, R, b

# A <- Pr A
# Pr_0 anulez elem de sub diag din coloanaa 0

def verificare_singularitate(R, n, epsilon):
    for i in range(n):
        if abs(R[i][i]) <= epsilon:
            # print(f"Matricea A initiala este singulara!")
            return False
    return True # nu e singulara

def rezolvare_sistem_householder_qr(R, b, n, epsilon, afisare):
    # substitutie inversa

    if afisare:
        print("Matricea R:\n", R)
        print("\nVectorul Q^Tb:\n", b)

    x_householder = np.zeros(n, dtype=float)

    for i in range(n-1, -1, -1): # pornesc de la n-1 pana la 0, pas -1
        suma = 0
        for j in range(i+1,n):
            suma += R[i][j] * x_householder[j]

        if abs(R[i][i]) <= epsilon:
            print("\nMatricea este singulara.\n")
            break

        x_householder[i] = (b[i] - suma) / R[i][i]

    print(f"\nSolutia sistemului folosind alg Householder QR:\n ", "x_householder = ", x_householder)
    return x_householder

def rezolvare_sistem_exclusiv_numpy_qr(A, b, afisare):
    Q, R = np.linalg.qr(A)

    if afisare:
        print(f"Matricea Q:\n {Q}")
        print(f"\nMatricea R:\n {R}")

    QTb = Q.T @ b
    if afisare:
        print(f"\nVectorul Q^Tb:\n {QTb}")

    x_numpy = np.linalg.solve(R, QTb)

    print(f"\nSolutia sistemului folosind biblioteca Numpy QR:\n ", "x_numpy = ", x_numpy)
    return x_numpy

"""
def rezolvare_sistem_numpy_qr(A, b, n, epsilon):
    Q, R = np.linalg.qr(A)
    print(f"Matricea Q:\n {Q}")
    print(f"\nMatricea R:\n {R}")

    x_numpy = np.zeros(n, dtype=float)
    
    for i in range(n-1, -1, -1):
        suma = 0
        for j in range(i+1,n):
            suma += R[i][j] * x_numpy[j]

        if abs(R[i][i]) <= epsilon:
            print("\nMatricea este singulara.\n")
            break

        x_numpy[i] = (b[i] - suma) / R[i][i]

    print(f"\nSolutia sistemului folosind biblioteca Numpy QR:\n ", "x_numpy = ", x_numpy)
    return x_numpy
"""

def calculare_erori(A_init, b_init, s, x_numpy, x_householder, epsilon):
    norma1 = np.linalg.norm(A_init @ x_householder - b_init, ord=2)
    print("||A_init * x_householder - b_init|| =", norma1)
    if norma1 > epsilon:
        print("\nEroare mare.\n")

    norma2 = np.linalg.norm(A_init @ x_numpy - b_init, ord=2)
    print("||A_init * x_numpy - b_init|| =", norma2)
    if norma2 > epsilon:
        print("\nEroare mare.\n")

    norma3_sus = np.linalg.norm(x_householder - s, ord=2)
    print("||x_householder - s|| =", norma3_sus)
    norma3_jos = np.linalg.norm(s, ord=2)
    print("||s|| =", norma3_jos)
    norma3 = norma3_sus / norma3_jos
    print("||x_householder - s|| / ||s|| =", norma3)
    if norma3 > epsilon:
        print("\nEroare mare.\n")

    norma4_sus = np.linalg.norm(x_numpy - s, ord=2)
    print("||x_numpy - s|| =", norma4_sus)
    print("||s|| =", norma3_jos)
    norma4 = norma4_sus / norma3_jos
    print("||x_numpy - s|| / ||s|| =", norma4)
    if norma4 > epsilon:
        print("\nEroare mare.\n")

def inversa_qr_householder(Q, R, n, epsilon, afisare):
    A_inversa_householder = np.zeros((n,n), dtype=float)

    if not verificare_singularitate(R, n, epsilon):
        print("\nMatricea A este singulara si nu putem calcula inversa\n")
        return None

    print("\nMatricea A nu este singulara si putem calcula inversa\n")

    for j in range(n):
        e_j = np.zeros(n, dtype=float) # baza canonica
        e_j[j] = 1.0

        b = Q.T @ e_j

        x = rezolvare_sistem_householder_qr(R, b, n, epsilon, afisare)

        for i in range(n):
            A_inversa_householder[i][j] = x[i] # in coloana j a inversei voi avea solutia sistemului Ax = e_j
                                                # deci pentru fiecare coloana rezolv n sisteme

        if afisare:
            print(f"\nColoana {j + 1} din A^(-1):\n", x)

    print(f"\nInversa matricei A folosind Householder:\n", A_inversa_householder)
    return A_inversa_householder

def inversa_qr_numpy(A):
    A = np.array(A, dtype=float)
    A_inversa_numpy = np.linalg.inv(A)

    print("\nInversa matricei A folosind Numpy:\n", A_inversa_numpy)
    return A_inversa_numpy

def randomizare_date(n):
    A = np.random.randn(n,n)
    s = np.random.randn(n)
    return A, s

def run():

    n = 3
    epsilon = 10e-7
    A_init = [
        [0, 0, 4],
        [1, 2, 3],
        [0, 1, 2]
    ]
    s_init = [3, 2, 1]
    start_time = time.time()
    """
    n = 10
    afisare = True
    if n > 100:
        afisare = False
    epsilon = 1e-6
    A_init, s_init = randomizare_date(n)
    """
    # afisari date initiale
    afisare = True
    if n > 100:
        afisare = False
    if afisare:
        print(f"Matricea A:\n {A_init}\n")
        print(f"Vectorul s:\n {s_init}\n")

    # punctul 1: calcularea vectorului b
    print("b = A * s")
    b = calcul_vector_b(A_init, s_init, afisare)
    print(f"Vectorul b:\n {b}\n")

    # punctul 2: descompunerea QR folosind alg lui Householder
    print("A = Q * R")
    print(f"Descompunerea QR a matricei A:\n")
    Q, R, b_householder = descompunere_householder_qr(A_init, n, b, epsilon, afisare)

    if verificare_singularitate(R, n, epsilon):
        print("Matricea A nu este singulara pentru ca nu exista elemente nule pe diagonala\n")
    else:
        print("Matricea A este singulara pentru ca exista minim 1 element nul pe diagonala\n")

    # punctul 3: rezolvarea sistemului liniar + norma
    print("A * x = b <=> R * x = Q.T * b")
    print("Rezolvarea sistemului prin doua metode:\n")

    print("Metoda Householder QR:\n")
    x_householder = rezolvare_sistem_householder_qr(R, b_householder, n, epsilon, afisare)
    print("\nMetoda Numpy QR:\n")
    x_numpy = rezolvare_sistem_exclusiv_numpy_qr(A_init, b, afisare)

    #norma_solutii = math.sqrt(sum((x_numpy[i] - x_householder[i]) ** 2 for i in range(n)))
    norma_solutii = np.linalg.norm(x_numpy - x_householder, ord=2)
    print("\nNorma euclidiana ||x_qr - x_householder|| =", norma_solutii)

    #norma = np.linalg.norm(x_numpy - x_householder, ord=2)
    #print("Norma euclidiana ||x_qr - x_householder|| =", norma)

    # punctul 4: afisarea erorilor

    print("\nErorile calculate:\n")
    calculare_erori(A_init, b, s_init, x_numpy, x_householder, epsilon)

    # punctul 5: comparare inversa matricii A folosind QR Householder vs inversa matricii A folosind QR Numpy

    A_inversa_householder = inversa_qr_householder(Q, R, n, epsilon, afisare)
    A_inversa_numpy = inversa_qr_numpy(A_init)

    norma_inverse = np.linalg.norm(A_inversa_householder - A_inversa_numpy, ord=2)
    print("\nNorma diferentei dintre cele doua inverse:\n", norma_inverse)

    end_time = time.time()
    print("\nTimp total de rulare:", end_time - start_time, "secunde")

if __name__ == "__main__":
    run()