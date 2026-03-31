import random
import numpy as np

def generare_matrice_random(p, n):
    A = []

    for i in range(p):
        linie = []
        for j in range(n):
            linie.append(random.uniform(0, 10))
        A.append(linie)

    return A

def generare_matrice_simetrica_random(n):
    A = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(i, n):
            valoare = random.uniform(0, 10)
            A[i][j] = valoare
            A[j][i] = valoare

    return A

def este_matrice_simetrica(A, n, epsilon = 1e-15):
    for i in range(n):
        for j in range(n):
            if abs(A[i][j] - A[j][i]) > epsilon:
                return False
    return True

# caut indicii celui mai mare element din afara diagonalei
# cum matricea e simetrica, caut doar sub diag
def gaseste_indici_pq_pentru_maxim(A, n):
    p = 1
    q = 0
    element_maxim = abs(A[p][q])
    for i in range(1, n):
        for j in range(i):
            if abs(A[i][j]) > element_maxim:
                element_maxim = abs(A[i][j])
                p = i
                q = j
    return p, q

def calculare_unghi_rotatie(A, p, q):
    a_pp = A[p][p]
    a_qq = A[q][q]
    a_pq = A[p][q]

    alfa = (a_pp - a_qq) / (2 * a_pq)

    # t in functie de semnul lui alfa
    if alfa >= 0:
        t = -alfa + np.sqrt(alfa * alfa + 1)
    else:
        t = -alfa - np.sqrt(alfa * alfa + 1)

    # constante
    c = 1 / np.sqrt(1 + t * t)
    s = t / np.sqrt(1 + t * t)

    return t, c, s

def metoda_jacobi(A, n, epsilon, kmax=10000):
    U = np.eye(n) # matricea identitate
    k = 0 # nr de pasi

    p, q = gaseste_indici_pq_pentru_maxim(A, n)

    # conditia de oprire: matricea e diagonala sau sunt deja prea multi pasi facuti
    while abs(A[p][q]) > epsilon and k <= kmax:
        t, c, s = calculare_unghi_rotatie(A, p, q)

        a_pp_vechi = A[p][p]
        a_qq_vechi = A[q][q]
        a_pq_vechi = A[p][q]

        # rotatie pentru toate coloanele in afara de p si q
        for j in range(n):
            if j != p and j != q:
                a_qj_vechi = A[q][j]
                a_pj_vechi = A[p][j]

                A[p][j] = c * a_pj_vechi + s * a_qj_vechi # rotatia efectiva
                A[j][p] = A[p][j] # pastrez conditia de simetrie

                A[q][j] = -s * a_pj_vechi + c * a_qj_vechi # rotatia efectiva
                A[j][q] = A[q][j] # pastrez conditia de simetrie

        # actualizare A (5)
        A[p][p] = a_pp_vechi + t * a_pq_vechi
        A[q][q] = a_qq_vechi - t * a_pq_vechi
        A[p][q] = 0
        A[q][p] = 0

        # actualizare U (7)
        # coloane U = vectori proprii aprox
        for i in range(n):
            u_ip_vechi = U[i][p]
            u_iq_vechi = U[i][q]

            U[i][p] = c * u_ip_vechi + s * u_iq_vechi
            U[i][q] = -s * u_ip_vechi + c * u_iq_vechi

        p, q = gaseste_indici_pq_pentru_maxim(A, n)
        k += 1

    return A, U, k

def norma_matriceala_jacobi(A_init, U, diagonala_A_final):
    diferenta = A_init @ U - U @ diagonala_A_final
    norma = np.linalg.norm(diferenta, ord=2)
    return norma

def este_matrice_pozitiv_definita(A_init, epsilon=1e-12):
    # calcul valori proprii
    valori_proprii = np.linalg.eigvals(A_init)

    # verific daca toate sunt > 0
    for valoare in valori_proprii:
        if valoare <= epsilon:
            return False

    return True

def metoda_choleski(A_init, epsilon, kmax=10000):
    for k in range(kmax):
        A_vechi = A_init.copy()

        # calculez factorizarea choleski A = L * L^T
        L = np.linalg.cholesky(A_init)

        # constructia matricei urmatoare k+1
        A_init = L.T @ L

        # verificare oprire
        if np.linalg.norm(A_init - A_vechi, ord=2) < epsilon:
            print("\nConvergenta atinsa la iteratia:", k)
            break

    return A_init, k

def calculare_rang_si_max_min(S):
    rang_matrice = 0
    valoarea_singulara_minima = None
    valoarea_singulara_maxima = None

    for valoare in S:
        if valoare > 0:
            rang_matrice += 1
            if valoarea_singulara_minima is None or valoare < valoarea_singulara_minima:
                valoarea_singulara_minima = valoare
            if valoarea_singulara_maxima is None or valoare > valoarea_singulara_maxima:
                valoarea_singulara_maxima = valoare

    return rang_matrice, valoarea_singulara_minima, valoarea_singulara_maxima

def construire_matrice_S_I(n, p, S, rang_matrice_A):
    S_I = np.zeros((n, p))

    for i in range(rang_matrice_A):
        if S[i] > 0:
            S_I[i][i] = 1 / S[i]

    return S_I

def run():
    n = 3
    print("n =", n)
    p = 4
    print("p =", p)
    if p < n:
        raise ValueError("\np trebuie sa fie >= n\n")

    epsilon = 1e-15
    print("\nEpsilon =", epsilon)

    A = np.array([
        [1, 1, 1],
        [1, 5, 5],
        [1, 5, 14],
        [1, 3, 4]
    ], dtype=float)
    print("\nMatricea A:\n", A)

    if p == n:
        # pct 1: metoda 1 de a construi o matrice diagonala
        # prin aproximarea valorilor proprii folosind metoda jacobi

        #A = generare_matrice_simetrica_random(n)

        if not este_matrice_simetrica(A, n):
            print("Matricea nu este simetrica si nu putem aplica metoda lui Jacobi!\n")
            return

        A_init = np.copy(A)

        A_final, U, k_jacobi = metoda_jacobi(A, n, epsilon)
        diagonala_A_final = np.diag(np.diag(A_final))

        print("\nAlgoritmul Jacobi s-a executat in", k_jacobi, "pasi")
        print("\nMatricea diagonala A_final:\n", A_final)
        print("\nMatricea ortogonala U (coloanele sunt aproximari ale vectorilor proprii):\n", U)
        print("\nValorile proprii aproximative de pe diagonala matricei A diagonala:\n", diagonala_A_final)

        print("\nNorma matriceala || A_init * U - U * diag_A || = ", norma_matriceala_jacobi(A_init, U, diagonala_A_final))

        # pct 2: metoda 2 de a construi o matrice diagonala folosind cholenski
        # prin calcularea sirurilor de matrice

        if not este_matrice_pozitiv_definita(A):
            print("\nMatricea nu este pozitiv definita si nu putem aplica algoritmul Cholesky!\n")
            return

        A_k, k_choleski = metoda_choleski(A_init, epsilon)

        print("\nAlgoritmul de descompunere Choleski s-a executat in", k_choleski, "pasi")
        print("\nMatricea diagonala A_k:\n", A_k)

    else:
        if p > n:
            #A = generare_matrice_random(p, n)
            print("\nMatricea A:\n", A)

            # valorile singulare ale matricei A
            # A = U * S * V.T
            U, S, V_transpus = np.linalg.svd(A, full_matrices=True)
            print("\nValorile singulare ale matricei A sunt:\n", S)

            # rangul matricei A
            rang_matrice_A, minim, maxim = calculare_rang_si_max_min(S)
            print("\nRangul matricei A:", rang_matrice_A)

            # numar de conditionare al matricei A
            numar_conditionare_matrice_A = maxim/minim
            print("Numarul de conditionare al matricei A este:\n", numar_conditionare_matrice_A)

            # pseudoinversa Moore-Penrose a matricei A
            S_I = construire_matrice_S_I(n, p, S, rang_matrice_A)
            print("\nMatricea S_I:\n", S_I)

            V = V_transpus.T
            A_I = V @ S_I @ U.T
            print("\nPseudoinversa Moore-Penrose A_I este:\n", A_I)

            # matricea pseudo-inversa in sensul celor mai mici patrate
            A_J = np.linalg.inv(A.T @ A) @ A.T
            print("\nMatricea pseudo-inversa in sensul celor mai mici patrate:\n", A_J)

            # norma
            norma = np.linalg.norm(A_I - A_J, ord=1)
            print("\n|| A_I - A_J ||1 =", norma)

if __name__ == "__main__":
    run()