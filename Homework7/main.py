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

def run():
    coef = [1.0, -6.0, 11.0, -6.0]

    eps = 1e-10

    R = compute_R(coef)

    print(f"Intervalul in care se gasesc radacinile functiei este: [-{R},{R}]")

    deriv = coef_deriv(coef)
    second_deriv = coef_deriv(deriv)

    print(f"Coeficientii primei derivate sunt: {deriv}")
    print(f"Coeficientii celei de-a doua derivate sunt: {second_deriv}")
run()