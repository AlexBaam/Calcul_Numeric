from pathlib import Path
'''
Functie folosita pentru a citi continutul unui fisier si a returna lungimea acestui fisier 
Luam in considerare faptul ca pe fiecare rand avem un singur numar 
'''
def file_content(file_path):
    f = open(file_path, 'r')
    current_count = len(f.readlines()) - 1 # fiindca avem un empty space la final incepem de la -1
    f.close()

    print("The number of elements in " + file_path.parent.name + "_" + file_path.name + " is equal to: " + str(current_count))
    return current_count

'''
Functie folosita pentru a verifica daca inantrul unor fisiere avem elemente nule
Facem asta prin comparatie cu epsilon ce e foarte mic
Ca sa nu verificam ultima linie sau linii ce pot fi goale folosim i != endline
'''
def nullity_check(file_path):
    epsilon = 1e-8

    f = open(file_path, 'r')
    for i in f.readlines():
        # Aici am nevoie de niste sugestii findca aceasta castare la float(i) reduce precizia, de asta si numarul meu e asa mic pentru epsilon
        # Ar parea ca numerele cu o perioada foarte mare precum .6666666666666 sunt reduse la .66 indiferent de ce ar avea in urma perioadei, si nu stiu unde poate duce asta la calcule
        # Exista posibilitatea unor erori daca as avea numere precum 0.0001111111111111111134523 sau ceva, si atunci el nu ar fi nul, dar reducerea acestuia la un nr mai mic de zecimale
        # Il poate transforma intr-un 0.00 si atunci poate imi zice ca am element nul desi nu am, this is bs tbh
        if i != '\n' and (abs(float(i)) < epsilon): # Verific pe baza unei precizii faptul ca am elemente nule
            print("There is an element in d0_" + file_path.name + " that is almost 0, that element is: " + str(i))
            f.close()
            return False

    f.close()
    print("There were no nule elements in d0_" + file_path.name)
    return True

'''
Functie ce ia valorile dintr-un fisier si le pune intr-un vector (lista)
Ne trebuie pentru gass-siedel
'''
def read_vector(file_path):
    values = []

    f = open(file_path, 'r')
    for line in f.readlines():
        if line != '\n': # Ignoram spatiile libere otherwise it will mess it up
            values.append(float(line))
    f.close()

    return values

'''
Functie in care aplicam metoda gauss-seidel pentru a rezolva sistemul Ax = b
Fiindca nu putem memora metricea complet folosim vecotri ptr fiecare dintre diagonale si vectorul b
n e marimea matricei (stabilita ptr intermediul dimensiunii d0), p si q sunt distantele diagonalelor fata de cea principala
kmax e nr maxim de iteratii ce il permitem, daca nu il oferim in cod e by default 10000
Epsilon e toleranta permisa intre 2 iteratii
Adica daca diferenta dintre 2 iteratii e prea apropiata de epsilon inseamna ca noi divergem'''
def gauss_seidel(d0, d1, d2, b, n, p, q, epsilon=1e-5, kmax=10000):
    # Vector solutie ce e initializat cu 0
    x = [0.0] * n

    k = 0
    delta = float('inf') # Ne asiguram ca bucla incepe macar o data fiindca daca delta e 0 atunci epsilon e mai mare
    # Reprezinta diferenta dintre doua iteratii consecutive

    while delta >= epsilon and k < kmax:
        # Aici salvam iteratia veche a algoritmului (ultimul vector solutie) ptr ca urmeaza sa updatam x
        x_old = x.copy()
        delta = 0.0 # In cadrul fiecarei iteratii readucem la 0 pentru a putea reface comparatiile

        for i in range(n):
            s = 0.0

            if i - p >= 0:
                s += d1[i - p] * x[i - p]

            if i + p < n:
                s += d1[i] * x_old[i + p]

            if i - q >= 0:
                s += d2[i - q] * x[i - q]

            if i + q < n:
                s += d2[i] * x_old[i + q]

            new_val = (b[i] - s) / d0[i]

            # DAca diferenta dintre modul de noua solutie si cea veche este mai mare decat delta atunci delta devine acea valoare
            diff = abs(new_val - x_old[i])
            if diff > delta:
                delta = diff

            x[i] = new_val

        # Incrementam numarul de iteratii realizat pana acum
        k += 1

        # Divergem in cazul in care delta devine prea mare (Peste 10^10)
        if delta > 1e10:
            return None, k

    # Daca atunci cand iesim din while delta e mai mic decat epsilon inseamna ca nu am ajuns la a diverge, deci returnam solutia
    if delta < epsilon:
        return x, k
    else:
        return None, k

'''
Functie pentru a calcula y = A * xGS (solutia Gauss-Siedel)
Acesta trebuie sa fie aproape de b ca valori
'''
def compute_y(d0, d1, d2, x, n, p, q):
    y = [0.0] * n

    for i in range(n):
        y[i] += d0[i] * x[i]

        if i < len(d1):
            y[i] += d1[i] * x[i + p]
            y[i + p] += d1[i] * x[i]

        if i < len(d2):
            y[i] += d2[i] * x[i + q]
            y[i + q] += d2[i] * x[i]

    return y

'''
Verificam diferenta dintre b si y ptr a vedea daca normele sunt destul de apropiate
'''
def infinity_norm(y, b, n):
    norm = 0.0

    for i in range(n):
        diff = abs(y[i] - b[i])
        if diff > norm:
            norm = diff

    return norm

def run():
    b_path = Path('b')
    d0_path = Path('d0')
    d1_path = Path('d1')
    d2_path = Path('d2')

    for b_file in b_path.iterdir():
        if b_file.is_file():
            file_name = b_file.name

            print("Processing file " + file_name)

            d0_file = d0_path / file_name
            d1_file = d1_path / file_name
            d2_file = d2_path / file_name

            b_elements_count = file_content(b_file)
            d0_elements_count = file_content(d0_file)
            d1_elements_count = file_content(d1_file)
            d2_elements_count = file_content(d2_file)

            if b_elements_count != d0_elements_count:
                print("The number of elements in b_" + file_name + " and d0_" + file_name + " is not equal, cannot solve the system")
                continue

            p = d0_elements_count - d1_elements_count
            q = d0_elements_count - d2_elements_count

            print("For file " + file_name + " we have: p = " + str(p) + ", q = " + str(q))

            if not nullity_check(d0_file):
                print("Cannot solve system for file " + file_name)
                print("")
                continue

            d0 = read_vector(d0_file)
            d1 = read_vector(d1_file)
            d2 = read_vector(d2_file)
            b = read_vector(b_file)

            x, k = gauss_seidel(d0, d1, d2, b, d0_elements_count, p, q)

            if x is not None:
                print("Gauss-Seidel converged for file " + file_name + " in " + str(k) + " iterations")

                y = compute_y(d0, d1, d2, x, d0_elements_count, p, q)

                norm = infinity_norm(y, b, d0_elements_count)
                print("The norm ||AxGS - b|| for file " + file_name + " is: " + str(norm))
            else:
                print("Gauss-Seidel diverged for file " + file_name + " after " + str(k) + " iterations")

            print("")
if __name__ == "__main__":
    run()