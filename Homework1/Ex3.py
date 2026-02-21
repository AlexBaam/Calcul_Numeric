import math
import random

import numpy as np

import sys

from Homework1.tangents.tan_by_fractions import aproximare_tan_fractii_continue
from Homework1.tangents.tan_by_polinoms import polinomial_tan

def compare_polinomial_tan(x):
    numpy_tan = np.tan(x)
    print("The tangent by NumPy is: ", numpy_tan)

    my_tan = polinomial_tan(x)
    print("The tangent by polinomial formula is: ", my_tan)

    abs_value = abs(numpy_tan - my_tan)

    print("The absolute value between them is: ", abs_value, "\n")

def compare_fraction_tan(x):
    my_tan = aproximare_tan_fractii_continue(x, 1e-15)
    tan = np.tan(x)

    print(f"Tangenta calculata cu numpy: {tan}")
    print(f"Tangenta aproximata prin fractii: {my_tan}")
    print(f"Diferenta: {abs(tan - my_tan)}\n")

def run():
    o = sys.stdout

    # Redirect stdout to a file
    with open('output.txt', 'w') as f:
        sys.stdout = f

        i = 1
        while i <= 100:
            print("Iteration: ", i)

            lower_bound = (math.pi / 2) * (-1)
            upper_bound = (math.pi / 2)

            print("This is lower_bound: ", lower_bound)
            print("This is upper_bound: ", upper_bound)

            x = random.uniform(lower_bound, upper_bound)

            print("This is the number: ", x, "\n")

            print(compare_polinomial_tan(x))
            print(compare_fraction_tan(x))

            i = i + 1

    # Restore stdout
    sys.stdout = o

print(run())