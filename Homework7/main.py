def compute_R(coef):
    """
    Pas 1: Calculam R astfel incat toate radacinile reale sa fie in [-R,R]
    Folosim formula R = (|a0| + A) / |a0|
    A = max{|ai|; i = 1, n}
    """
    a0 = coef[0]
    if a0 == 0:
        print("Nu putem avea a0 = 0 fiindca polinomul nu mai este de grad potrivit.")
        return 0.0

    if len(coef) == 1:
        return 0.0

    A = -9999999

    for c in coef[1:]:
        A = max(abs(c), A) #     A = max{|ai|; i = 1, n}
    R = (abs(a0) + A) / abs(a0)
    return R

def coef_deriv(coef):
    """
    Pas 2: Calculam coeficientii derivati pentru fiecare termen al polinomului.
    Luam fiecare coeficient, nr de coeficienti ne spune puterea la care se afla polinomul (4 coeficienti inseamna ca e polinom de gradul 3)
    Un exemplu ar fi:
    [a0, a1, a2, a3] => [a0*3, a1*2, a2*1, a3*0]
    """
    grad = len(coef) - 1

    if grad == 0:
        return [0.0]

    deriv = [] # Aici vom salva o lista cu coeficientii derivatei
    for i in range(len(coef) - 1): # Scadem 1 pentru a tot scurta cu fiecare derivata array deriv, motivul este optimizare
        power = grad - i
        deriv.append(coef[i] * power)

    return deriv

def horner_pol(coef, x):
    """
    Pas 3: Aducem polinomul la forma lui Horner ce ia un polinom de forma P(x) = a0 * x^2 + a1 * x + a2  la forma horner(P(x)) = (a0*x + a1)x + a2
    Asta face calculele sa fie mai simple, nu mai lucram cu puteri, doar inmultiri recursive
    Intai calculam bucata horner_pol_x = a0*x + a1, urmatoarea recursie calculam horner_pol_x = horner_pol_x*x + a2
    """

    # Asta e variabila ptr a calcula valoarea polinomului intr-un punct, intai o initializam cu a0 ptr a putea urma forma de mai sus
    # Ce fac aici e echivalentul lui b0, idk numele de horner_pol_x pare mai intuitiv venind de la horner polinom on X
    horner_pol_x = coef[0]

    for val in coef[1:]:
        # Apoi aici fac spre exemplu b1 = a1 + b0 * v
        # v fiind o valoarea fixa aleasa lui x
        horner_pol_x = horner_pol_x*x + val

    return horner_pol_x

def horner_all(pol, deriv_pol, second_deriv_pol, x):
    """
    Spocul acestei functii este doar sa calculam valoarea pentru un x oarecare a polinomului, polinomuliui derivat si cel dublu derivat
    """

    pol_x = horner_pol(pol, x)
    pol_deriv_x = horner_pol(deriv_pol, x)
    pol_double_deriv_x = horner_pol(second_deriv_pol, x)

    return pol_x, pol_deriv_x, pol_double_deriv_x

def run():
    coef = [1.0, -6.0, 11.0, -6.0]

    eps = 1e-10

    R = compute_R(coef)

    print(f"Intervalul in care se gasesc radacinile functiei este: [-{R},{R}]")

    print("Coeficientii polinomului sunt: ", coef)

    deriv = coef_deriv(coef)
    second_deriv = coef_deriv(deriv)

    print(f"Coeficientii primei derivate sunt: {deriv}")
    print(f"Coeficientii celei de-a doua derivate sunt: {second_deriv}")

    x = 1
    pol_x, pol_deriv_x, pol_double_deriv_x = horner_all(coef, deriv, second_deriv, x)

    print(f"Pentru x = {x} avem urmatoarele valori ptr polinom: ")
    print(f"P({x}) = {pol_x}")
    print(f"P'({x}) = {pol_deriv_x}")
    print(f"P''({x}) = {pol_double_deriv_x}")

run()