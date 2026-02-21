def find_u():
    m = 0
    u = pow(10, -m)
    while 1.0 + u != 1.0:
        m = m + 1
        u = pow(10, -m)

    return u * 10

print("Raspuns exercitiul 1:", find_u())

#Raspunsuri precum "1e-15" inseamna  1 * 10^(-15)