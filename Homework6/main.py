import numpy as np
import matplotlib.pyplot as plt

# generare noduri interioare aleatoare si valorile lor pentru f aleasa
def generare_noduri_x_si_valori_y(x_0, x_n, n, f):
    x_interior = np.sort(np.random.uniform(x_0, x_n, n - 1))
    x_i = np.concatenate(([x_0], x_interior, [x_n]))
    y_i = f(x_i)
    return x_i, y_i

def generare_functie(x):
    return x**4 - 12*x**3 + 30*x**2 + 12
    #return x**3 + 3*x**2 - 5*x + 12

def afisare_functie():
    return "x^4 - 12x^3 + 30x^2 + 12"
    #return "x^3 + 3x^2 - 5x + 12"

def verificare_x_barat(x_barat, x_i, epsilon = 1e-12):
    return not np.any(np.abs(x_i - x_barat) < epsilon)
    # np.any intreaba daca exista vreun true si il intoarce true cand gaseste ceva
    # exista vreun x_i egal cu x_barat? daca da, return true
    # true - x_barat e valid
    # false - nu e valid

# Ba = f => a sunt coeficientii/solutia sistemului
def construire_sistem_polinom(x_i, y_i, m):
    B = np.zeros((m + 1, m + 1))
    f = np.zeros(m + 1)
    for i in range(m + 1):
        for j in range(m + 1):
            B[i][j] = np.sum(x_i ** (i + j))
        f[i] = np.sum(y_i * x_i ** i)
    return B, f

# gasirea coeficientilor a_i prin rezolvarea sistemului
def rezolvare_sistem_polinom(x_i, y_i, m):
    B, f = construire_sistem_polinom(x_i, y_i, m)
    a_i = np.linalg.solve(B, f)
    return a_i

def rezolvare_schema_horner(a_i, x_barat):
    # eu am elementele in vectorul a_i de la x^0 la cel mai mare
    P_x = a_i[-1] # pornesc de la coeficientului termenului cu grad maxim / adica ultimul element din vector
    # iau pe rand restul coeficientilor
    # pornesc de la penultimul element pentru ca pe ultimul l am folosit deja
    # scad -1 la fiecare iteratie ca merg de la dreapta la stanga
    # am opresc inainte de -1, execut 0 si stop
    for i in range(len(a_i) - 2, -1, -1):
        P_x = P_x * x_barat + a_i[i]
    return P_x

def derivata_functie(x):
    return 4*x**3 - 36*x**2 + 60*x

# x_i+1 - x_i
def calculare_h(x_i):
    h = np.zeros(len(x_i) - 1)
    for i in range(len(x_i) - 1):
        h[i] = x_i[i + 1] - x_i[i]
    return h

def construire_sistem_spline(x_i, y_i, da, db):
    h = calculare_h(x_i)
    n = len(x_i) - 1

    H = np.zeros((n + 1, n + 1))
    f = np.zeros(n + 1)

    H[0][0] = 2 * h[0]
    H[0][1] = h[0]
    f[0] = 6 * ((y_i[1] - y_i[0]) / h[0])

    for i in range(1, n):
        H[i][i - 1] = h[i - 1]
        H[i][i] = 2 * (h[i - 1] + h[i])
        H[i][i + 1] = h[i]
        f[i] = 6 * (((y_i[i + 1] - y_i[i]) / h[i]) - ((y_i[i] - y_i[i - 1]) / h[i - 1]))

    H[n][n - 1] = h[n - 1]
    H[n][n] = 2 * h[n - 1]
    f[n] = 6 * (db - (y_i[n] - y_i[n - 1]) / h[n - 1])

    return H, f

def rezolvare_sistem_spline(x_i, y_i, da, db):
    H, f = construire_sistem_spline(x_i, y_i, da, db)
    A_i = np.linalg.solve(H, f)
    return A_i

def calculare_b(x_i, y_i, A_i, h_i, i):
    prima_fractie = (y_i[i + 1] - y_i[i]) / h_i[i]
    a_doua_fractie = (h_i[i] * (A_i[i + 1] - A_i[i])) / 6
    b_i = prima_fractie - a_doua_fractie
    return b_i

def calculare_c(x_i, y_i, A_i, h_i, i):
    prima_fractie = ((x_i[i + 1] * y_i[i]) - (x_i[i] * y_i[i + 1])) / h_i[i]
    a_doua_fractie = (h_i[i] * ((x_i[i + 1] * A_i[i]) - (x_i[i] * A_i[i + 1]))) / 6
    c_i = prima_fractie - a_doua_fractie
    return c_i

def verificare_interval(punct_interval, start_interval, end_interval):
    if punct_interval < start_interval or punct_interval > end_interval:
        return False
    return True

def rezolvare_spline(x_i, y_i, A_i, x_barat):
    h_i = calculare_h(x_i)

    for i in range(len(x_i) - 1):
        b_i = calculare_b(x_i, y_i, A_i, h_i, i)
        c_i = calculare_c(x_i, y_i, A_i, h_i, i)

        prima_fractie = (((x_barat - x_i[i]) ** 3) * A_i[i + 1]) / (6 * h_i[i])
        a_doua_fractie = (((x_i[i + 1] - x_barat) ** 3) * A_i[i]) / (6 * h_i[i])

        S_x = prima_fractie + a_doua_fractie + b_i * x_barat + c_i
        return S_x

def citire_date_din_fisier(nume_fisier):
    with open(nume_fisier, "r") as f:
        x_0 = int(f.readline().strip())
        x_n = int(f.readline().strip())
        n = int(f.readline().strip())
        x_barat = float(f.readline().strip())
        da = float(f.readline().strip())
        db = float(f.readline().strip())

    return x_0, x_n, n, x_barat, da, db

def run():
    # date de intrare de la tastatura
    x_0 = float(input("x_0 = "))
    x_n = float(input("x_n = "))
    if x_0 >= x_n:
        raise ValueError("x_0 trebuie sa fie < x_n")

    n = int(input("n = "))

    # generarea nodurilor xi si a valorilor yi
    x_i, y_i = generare_noduri_x_si_valori_y(x_0, x_n, n, generare_functie)
    print("\nx_i = ", x_i)
    print("\ny_i = ", y_i)

    print("\nFunctia f(x) = ", afisare_functie())

    # PUNCTUL 1

    print("\nAproximare polinomiala calculata cu metoda celor mai mici patrate:")

    # gradul polinomului
    m = np.random.randint(1, 6)
    print("\nGradul ales pentru aproximare: ", m)

    # construirea polinomului
    a_i = rezolvare_sistem_polinom(x_i, y_i, m)
    print("\nCoeficientii polinomului a_i, de la cel mai mic coeficient la cel mai mare: \n", a_i)

    x_barat = float(input("x_barat = "))
    # verific ca x_barat sa fie != de orice x_i
    while not verificare_x_barat(x_barat, x_i):
        print("x_barat trebuie sa fie diferit de toate valorile x_i")
        x_barat = float(input("x_barat = "))

    P_x_barat = rezolvare_schema_horner(a_i, x_barat)
    print("\nPm(x_barat) = ", P_x_barat)

    f_x_barat = generare_functie(x_barat)
    print("\nf(x_barat) = ", f_x_barat)

    diferenta_polinom_functie = abs(P_x_barat - f_x_barat)
    print("\n| Pm(x_barat) - f(x_barat) | = ", diferenta_polinom_functie)

    suma_diferentelor_noduri_valori = 0
    for i in range(len(x_i)):
        P_x_i = rezolvare_schema_horner(a_i, x_i[i])
        diferenta_noduri_valori = abs(P_x_i - y_i[i])
        suma_diferentelor_noduri_valori += diferenta_noduri_valori

    print("\nSuma diferentei absolute dintre Pm(x_i) si y_i = ", suma_diferentelor_noduri_valori)

    # PUNCTUL 2

    print("\nAproximare folosind functiile spline cubice de clasa C^2:")

    da = 0
    db = 8

    A_i = rezolvare_sistem_spline(x_i, y_i, da, db)
    print("\nCoeficientii A_i pentru functiile spline cubice:\n", A_i)

    if verificare_interval(x_barat, x_0, x_n) == False:
        raise ValueError("\nx_barat nu apartine intervalului [a,b], cu a = x_0, b = x_n")

    S_x_barat = rezolvare_spline(x_i, y_i, A_i, x_barat)
    print("\nSf(x_barat) = ", S_x_barat)

    print("\nf(x_barat) = ", f_x_barat)

    diferenta_spline_functie = abs(S_x_barat - f_x_barat)
    print("\n| Sf(x_barat) - f(x_barat) | = ", diferenta_spline_functie)

    # PUNCTUL 3

    # Graficul pentru Pm(x)
    x_valori = np.linspace(x_0, x_n, 500)
    Pm_valori = [rezolvare_schema_horner(a_i, x) for x in x_valori]

    plt.figure(figsize=(10, 6))
    plt.plot(x_valori, generare_functie(x_valori), label="f(x) - Functia originala", color='blue', linestyle='dashed')
    plt.plot(x_valori, Pm_valori, label=f"P{m}(x) - Aproximatia polinomiala", color='red')
    plt.scatter(x_i, y_i, color='black', label="Punctele de interpolare")
    plt.title("Interpolare polinomiala cu metoda celor mai mici patrate")
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.show()

    # Graficul pentru Sf(x)

    Sf_valori = [rezolvare_spline(x_i, y_i, A_i, x) for x in x_valori]

    plt.figure(figsize=(10, 6))
    plt.plot(x_valori, generare_functie(x_valori), label="f(x) - Functia originala", color='blue', linestyle='dashed')
    plt.plot(x_valori, Sf_valori, label="Sf(x) - Aproximatia cu functii spline cubice", color='green')
    plt.scatter(x_i, y_i, color='black', label="Punctele de interpolare")
    plt.title("Interpolare cu functii spline cubice de clasa C^2")
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.show()

    """
    x_valori = np.linspace(x_0, x_n, 500)
    f_valori = generare_functie(x_valori)
    Pm_valori = [rezolvare_schema_horner(a_i, x) for x in x_valori]
    Sf_valori = [rezolvare_spline(x_i, y_i, A_i, x) for x in x_valori]

    plt.figure(figsize=(10, 6))
    plt.plot(x_valori, f_valori, label="f(x) - Functia originala", color='blue', linestyle='dashed')
    plt.plot(x_valori, Pm_valori, label=f"P{m}(x) - Aproximatia polinomiala", color='red')
    plt.plot(x_valori, Sf_valori, label="Sf(x) - Aproximatia cu functii spline cubice", color='green')
    plt.scatter(x_i, y_i, color='black', label="Punctele date")

    plt.title("Graficul functiei f si al aproximarilor Pm si Sf")
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.show()
    """

if __name__ == "__main__":
    run()