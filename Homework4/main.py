from pathlib import Path

def file_content(file_path):
    f = open(file_path, 'r')
    current_count = len(f.readlines()) - 1 # fiindca avem un empty space la final incepem de la -1
    f.close()

    print("The number of elements in " + file_path.parent.name + "_" + file_path.name + " is equal to: " + str(current_count))
    return current_count

def nullity_check(file_path):
    epsilon = 1e-4

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

def read_vector(file_path):
    values = []

    f = open(file_path, 'r')
    for line in f.readlines():
        if line != '\n':
            values.append(float(line))
    f.close()

    return values

def gauss_seidel(d0, d1, d2, b, n, p, q, epsilon=1e-5, kmax=10000):
    x = [0.0] * n

    k = 0
    delta = float('inf')

    while delta >= epsilon and k < kmax:
        x_old = x.copy()
        delta = 0.0

        for i in range(n):
            s = 0.0

            # stanga p
            if i - p >= 0:
                s += d1[i - p] * x[i - p]

            # dreapta p
            if i + p < n:
                s += d1[i] * x_old[i + p]

            # stanga q
            if i - q >= 0:
                s += d2[i - q] * x[i - q]

            # dreapta q
            if i + q < n:
                s += d2[i] * x_old[i + q]

            new_val = (b[i] - s) / d0[i]

            diff = abs(new_val - x_old[i])
            if diff > delta:
                delta = diff

            x[i] = new_val

        k += 1

        if delta > 1e10:
            return None, k

    if delta < epsilon:
        return x, k
    else:
        return None, k

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
                print("Vector y = A * xGS was computed for file " + file_name)

                norm = infinity_norm(y, b, d0_elements_count)
                print("The infinity norm ||AxGS - b||∞ for file " + file_name + " is: " + str(norm))
            else:
                print("Gauss-Seidel diverged for file " + file_name + " after " + str(k) + " iterations")

            print("")
if __name__ == "__main__":
    run()