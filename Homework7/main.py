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

def newton_met(pol, deriv_pol, x0, eps, kmax):
    x = x0
    k = 0

    while k < kmax:
        pol_x = horner_pol(pol, x)
        pol_deriv_x = horner_pol(deriv_pol, x)

        if abs(pol_deriv_x) < eps:
            return x, k, False

        # Impartirea din formula lui Newton ce trebuie scazuta din X
        impart = pol_x / pol_deriv_x

        # DACA REZULTATUL IMPARTIRII E FOARTE MARE INSEAMNA CA AM AVUT UN SALT URIAS CEEA CE INSEAMNA DIVERGENTA
        if abs(impart) > 1e8:
            return x, k, False

        x = x - impart # Actualizam aproximarea solutiei
        k = k + 1

        if abs(impart) < eps:
            return x, k, True

    return x, k, False

def oliver_met(pol, deriv_pol, second_deriv_pol, x0, eps, kmax):
    x = x0
    k = 0
    while k < kmax:
        pol_x, pol_deriv_x, pol_double_deriv_x = horner_all(pol, deriv_pol, second_deriv_pol, x)

        if abs(pol_deriv_x) < eps:
            return x, k, False

        ck = compute_ck(pol_x, pol_deriv_x, pol_double_deriv_x)

        impart = pol_x / pol_deriv_x + 0.5 * ck

        if abs(impart) > 1e8:
            return x, k, False

        x= x - impart
        k = k + 1

        if abs(impart) < eps:
            return x, k, True

    return x, k, False

def compute_ck(pol_x, pol_deriv_x, pol_double_deriv_x):
    """
    Calculam ck din formula lui Oliver
    """

    sqrd_pol = pol_x**2
    trpld_deriv = pol_deriv_x**3

    return sqrd_pol * pol_double_deriv_x / trpld_deriv

def generate_start_points(points_nr, R):
    start_points = []

    if points_nr <= 0:
        return start_points

    step = R * 3 / points_nr

    current_step = -1 * R

    for i in range(points_nr):

        if current_step > R:
            break

        start_points.append(current_step)
        current_step = current_step + step

    return start_points

def compare_steps(newton_steps, oliver_steps):
    if newton_steps < oliver_steps:
        return "Newton"
    elif newton_steps > oliver_steps:
        return "Oliver"
    else:
        return "Equal"

def check_if_different(new_root, root_list, eps):
    for root in root_list:
        if abs(new_root - root) < eps:
            return False

    return True

def different_new_ol(newton_root, olver_root, eps):
    if abs(newton_root - olver_root) < eps:
        return False
    else:
        return True

def add_root_to_list(new_root, root_list, eps):
    if check_if_different(new_root, root_list, eps):
        root_list.append(new_root)

def write_in_file(filename, roots):
    with open(filename, "w") as f:
        for root in roots:
            f.write(f"{root}\n")

        f.close()

def run():
    coef = [1.0, -6.0, 11.0, -6.0]

    eps = 1e-10

    R = compute_R(coef)

    print(f"Intervalul in care se gasesc radacinile functiei este: [-{R},{R}]")

    print(f"\nCoeficientii polinomului sunt: {coef}")

    deriv = coef_deriv(coef)
    second_deriv = coef_deriv(deriv)

    print(f"Coeficientii primei derivate sunt: {deriv}")
    print(f"Coeficientii celei de-a doua derivate sunt: {second_deriv}")

    x = 1
    pol_x, pol_deriv_x, pol_double_deriv_x = horner_all(coef, deriv, second_deriv, x)

    print(f"\nPentru x = {x} avem urmatoarele valori ptr polinom: ")
    print(f"P({x}) = {pol_x}")
    print(f"P'({x}) = {pol_deriv_x}")
    print(f"P''({x}) = {pol_double_deriv_x}")

    x0 = generate_start_points(300, R)
    max_steps = 1000

    print(f"\nVom itera prin urmatoarele puncte x0: {x0}")
    print(f"Numarul de iteratii ce il realizam este urmatorul: {len(x0)}")

    root_list = []

    for value in x0:
        root_newton, steps_newton, did_newton_converge = newton_met(coef, deriv, value, eps, max_steps)

        if did_newton_converge:
            print(f"\nMetoda lui Newton a convers la solutia {root_newton} in {steps_newton} pasi pentru x0 = {value}")
        else:
            print(f"\nMetoda lui Newton a divers dupa {steps_newton} pasi pentru x0 = {value}")


        root_oliver, steps_oliver, did_converge_oliver = oliver_met(coef, deriv, second_deriv, value, eps, max_steps)

        if did_converge_oliver:
            print(f"Metoda lui Oliver a convergent la solutia {root_oliver} in {steps_oliver} pasi pentru x0 = {value}")
        else:
            print(f"Metoda lui Oliver a divergent dupa {steps_oliver} pasi pentru x0 = {value}")

        if did_converge_oliver and did_newton_converge:
            print(f"Metoda ce a convers mai repede este: {compare_steps(steps_newton, steps_oliver)}")

            if different_new_ol(root_newton, root_oliver, eps):
                add_root_to_list(root_newton, root_list, eps)
                add_root_to_list(root_oliver, root_list, eps)
            else:
                add_root_to_list(root_newton, root_list, eps)

    write_in_file("roots.txt", root_list)
run()