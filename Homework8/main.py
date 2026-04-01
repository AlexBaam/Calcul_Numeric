import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def functia_l(w):
    w0, w1 = w
    return -np.log(1 - sigmoid(w0 - w1)) - np.log(sigmoid(w0 + w1))

def gradient_functie_l(w):
    w0, w1 = w
    return np.array([
        sigmoid(w0 - w1) + sigmoid(w0 + w1) - 1,
        sigmoid(w0 + w1) - sigmoid(w0 - w1) - 1
    ])

def functia_F1(x):
    x1, x2 = x
    return x1**2 + x2**2 - 2*x1 - 4*x2 - 1

# formula analitica gradient => DIN PDF
def gradient_functie_F1(x):
    x1, x2 = x
    return np.array([
        2 * x1 - 2,
        2 * x2 - 4
    ])

def functia_F2(x):
    x1, x2 = x
    return 3*x1**2 - 12*x1 + 2*x2**2 + 16*x2 - 10

def gradient_functie_F2(x):
    x1, x2 = x
    return np.array([
        6*x1 - 12,
        4*x2 + 16
    ])

def functia_F3(x):
    x1, x2 = x
    return x1**2 - 4*x1*x2 + 4.5*x2**2 - 4*x2 + 3

def gradient_functie_F3(x):
    x1, x2 = x
    return np.array([
        2*x1 - 4*x2,
        -4*x1 + 9*x2 - 4
    ])

def functia_F4(x):
    x1, x2 = x
    return x1**2*x2 - 2*x1*x2**2 + 3*x1*x2 + 4

def gradient_functie_F4(x):
    x1, x2 = x
    return np.array([
        2*x1*x2 - 2*x2**2 + 3*x2,
        x1**2 - 4*x1*x2 + 3*x1
    ])

def gradient_aproximativ_functie_F(Functia_F, x, h): # h e pasul
    gradient = np.zeros_like(x)
    n = len(x)

    """
    pentru fiecare variabila calculez derivata partiala aaproximativa
    
    am punctul (1,2)
    ptr i=0 => x1 = [1+2h, 2]
    ptr i=1 => x1 = [1, 2+2h] etc
    
    puncte in jurul lui x pentru a aproxima mai bine derivata
    """
    for i in range(n):
        x1 = np.copy(x)
        x1[i] += 2 * h # dreapta

        x2 = np.copy(x)
        x2[i] += h # ++ dreapta

        x3 = np.copy(x)
        x3[i] -= h # stanga

        x4 = np.copy(x)
        x4[i] -= 2 * h # ++ stanga

        # valorile functiei in cele 4 puncte alese
        F1 = Functia_F(x1)
        F2 = Functia_F(x2)
        F3 = Functia_F(x3)
        F4 = Functia_F(x4)

        # derivata partiala pentru x_i
        gradient[i] = (-F1 + 8*F2 - 8*F3 + F4) / (12*h)

    return gradient

def metoda_gradient_descendent(functia_F, gradient_functie_F, n=2, h=1e-6, rata_invatare=1e-3, foloseste_bkt_line_search=False, epsilon=1e-6, kmax=30000, beta=0.8, foloseste_gradient_aproximativ=False): # x0=None
    x = np.random.uniform(-1, 1, n) # se aleg random elemnetele vectorului initial x

    """
    if x0 is None:
        x = np.random.uniform(-1, 1, n)
    else:
        x = np.array(x0, dtype=float)
    """

    k = 0

    while True:
        # calculeaza gradientul
        if foloseste_gradient_aproximativ == True:
            gradient = gradient_aproximativ_functie_F(functia_F, x, h)
        else:
            gradient = gradient_functie_F(x)

        # calculeaza rata de invatare
        rata_invatare_pas_k = rata_invatare

        # bkt line search pentru ajustarea ratei de invatare
        if foloseste_bkt_line_search == True:
            rata_invatare_pas_k = 1
            p = 1

            while functia_F(x - rata_invatare_pas_k * gradient) > functia_F(x) - (rata_invatare_pas_k / 2) * np.linalg.norm(gradient)**2 and p < 8:
                rata_invatare_pas_k *= beta
                p = p + 1

        x = x - rata_invatare_pas_k * gradient
        k = k + 1

        # conditia de oprire while
        if not (rata_invatare_pas_k * np.linalg.norm(gradient) <= 10**10 and k <= kmax and rata_invatare_pas_k * np.linalg.norm(gradient) >= epsilon):
            break

    if rata_invatare_pas_k * np.linalg.norm(gradient) <= epsilon:
        return x, k

    return None, k

def comparare_gradienti(
    functia_F,
    gradient_functie_F,
    nume_functie,
    n=2,
    h=1e-6,
    rata_invatare=1e-3,
    foloseste_bkt_line_search=False,
    epsilon=1e-6,
    kmax=30000,
    beta=0.8
):
    print("-" * 100)
    print(f"Comparatie pentru {nume_functie}")
    print("-" * 100)

    """
    # acelasi punct initial pentru ambele metode
    x0 = np.random.uniform(-1, 1, n)
    print(f"Punct initial comun: {x0}")
    """

    # rulare cu gradient analitic
    punct_analitic, iteratii_analitic = metoda_gradient_descendent(
        functia_F,
        gradient_functie_F,
        n=n,
        h=h,
        rata_invatare=rata_invatare,
        foloseste_bkt_line_search=foloseste_bkt_line_search,
        epsilon=epsilon,
        kmax=kmax,
        beta=beta,
        foloseste_gradient_aproximativ=False,
        #x0=x0
    )

    # rulare cu gradient aproximativ
    punct_aproximativ, iteratii_aproximativ = metoda_gradient_descendent(
        functia_F,
        gradient_functie_F,
        n=n,
        h=h,
        rata_invatare=rata_invatare,
        foloseste_bkt_line_search=foloseste_bkt_line_search,
        epsilon=epsilon,
        kmax=kmax,
        beta=beta,
        foloseste_gradient_aproximativ=True,
        #x0=x0
    )

    print("Gradient analitic:")
    print(f"   Punct minim gasit: {punct_analitic}")
    print(f"   Numar iteratii: {iteratii_analitic}")
    if punct_analitic is not None:
        print(f"   Valoarea functiei: {functia_F(punct_analitic)}")
    else:
        print("   Metoda a fost divergenta.")

    print()

    print("Gradient aproximativ:")
    print(f"   Punct minim gasit: {punct_aproximativ}")
    print(f"   Numar iteratii: {iteratii_aproximativ}")
    if punct_aproximativ is not None:
        print(f"   Valoarea functiei: {functia_F(punct_aproximativ)}")
    else:
        print("   Metoda a fost divergenta.")

    print()

    if punct_analitic is not None and punct_aproximativ is not None:
        diferenta_puncte = np.linalg.norm(punct_analitic - punct_aproximativ)
        diferenta_valori = abs(functia_F(punct_analitic) - functia_F(punct_aproximativ))

        print("Comparatie finala:")
        print(f"   Diferenta intre punctele obtinute: {diferenta_puncte}")
        print(f"   Diferenta intre valorile functiei: {diferenta_valori}")

        if iteratii_analitic < iteratii_aproximativ:
            print("   Gradientul analitic a avut nevoie de mai putine iteratii.")
        elif iteratii_aproximativ < iteratii_analitic:
            print("   Gradientul aproximativ a avut nevoie de mai putine iteratii.")
        else:
            print("   Cele doua variante au avut acelasi numar de iteratii.")
    else:
        print("Comparatia completa nu se poate face deoarece una dintre metode sau ambele au fost divergente.")

    print()

def run():
    functii = [
        (functia_l, gradient_functie_l, "Functia l"),
        (functia_F1, gradient_functie_F1, "Functia F1"),
        (functia_F2, gradient_functie_F2, "Functia F2"),
        (functia_F3, gradient_functie_F3, "Functia F3"),
        (functia_F4, gradient_functie_F4, "Functia F4")
    ]

    cazuri_testare = [
        ("Rata de invatare constanta", False),
        ("Rata de invatare updatata cu backtracking line search", True)
    ]

    for nume_caz, foloseste_bkt_line_search in cazuri_testare:
        print("\n")
        print(nume_caz)
        print("\n")

        for functie, gradient_functie, nume_functie in functii:
            comparare_gradienti(
                functie,
                gradient_functie,
                nume_functie,
                n=2,
                h=1e-6,
                rata_invatare=1e-3,
                foloseste_bkt_line_search=foloseste_bkt_line_search,
                epsilon=1.1e-5,
                kmax=30000,
                beta=0.8
            )

        print("\n")

if __name__ == '__main__':
    run()