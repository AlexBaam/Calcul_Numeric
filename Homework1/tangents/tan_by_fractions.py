def aproximare_tan_fractii_continue(x, epsilon):
    mic = 1e-12
    f = mic
    C = f # numarator
    D = 0 # numitor
    j = 1
    # j=1
    while True:
        if j == 1:
            a_j = x
            b_j = 1
        else:
            a_j = -(x**2) # variabila initiala ca sa nu mai calculez la fiecare iteratie
            b_j = 2 * j - 1 # nr impare

        D = b_j + a_j * D
        if D == 0:
            D = mic

        C = b_j + a_j / C
        if C == 0:
            C = mic

        D = 1 / D
        delta = C * D
        f = delta * f

        if abs(delta - 1.0) < epsilon:
            break
        j = j + 1

    return f