import math
import random

import numpy as np

import sys
import time

from Homework1.tangents.tan_by_fractions import aproximare_tan_fractii_continue
from Homework1.tangents.tan_by_polinoms import polinomial_tan, better_polinomial_tan

def normalize_x(x):
    # perioada tangentei este pi, astfel daca luam x si il impartim la pi
    # numarul ramas ca rest este un x in  intervalul [0, pi)
    x = x % math.pi

    # valorile inca pot fi prea mari
    # reducem la intervalul (-pi/2, 0], cum se intampla asta? PAI DOAR DACA VALOAREA E PESTE pi/2 SCAD PI SI AJUNG LA -pi/2
    if x > math.pi/2:
        x = x - math.pi

    epsilon = 1e-15 # Definim un epsilon foarte mic
    if abs(abs(x) - math.pi / 2) < epsilon: # Daca diferenta absoluta dintre x si pi/2 este mai mica decat acest epsilon,
        # le consideram prea apropiate
        if x > 0:
            return float('inf')
        else:
            return float('-inf')

    return x

def compare_polinomial_tan(x):
    time_start_numpy = time.time()

    numpy_tan = np.tan(x)
    print("The tangent by NumPy is: ", numpy_tan)

    time_end_numpy = time.time()

    time_to_compute_numpy = time_end_numpy - time_start_numpy

    time_start_polinomial = time.time()

    my_tan = polinomial_tan(x)
    print("The tangent by polinomial formula is: ", my_tan)

    time_end_polinomial = time.time()

    time_to_compute_polinomial = time_end_polinomial - time_start_polinomial

    time_start_better_polinomial = time.time()

    my_better_tan = better_polinomial_tan(x)
    print("The more accurate tangent by polinomial formula is: ", my_better_tan, "\n")

    time_end_better_polinomial = time.time()

    time_to_compute_bettter_polinomial = time_end_better_polinomial - time_start_better_polinomial

    print("Time to compute NumPy: ", time_to_compute_bettter_polinomial)
    print("Time to compute polinomial: ", time_to_compute_polinomial)
    print("Time to compute optimised polinomial: ", time_to_compute_bettter_polinomial, "\n")

    is_numpy_faster = time_to_compute_polinomial > time_to_compute_numpy

    abs_value = abs(numpy_tan - my_tan)
    abs_value_optimised = abs(numpy_tan - my_better_tan)

    print("The absolute value between NumPy and Polinomial is: ", abs_value)
    print("The absolute value between Numpy and Optimised Polinomial is: ", abs_value_optimised)
    print("The faster method of computing the tangent is numpy? ", is_numpy_faster, "\n")

    return abs_value, abs_value_optimised, time_to_compute_polinomial

def compare_fraction_tan(x):
    time_start_numpy = time.time()

    tan = np.tan(x)
    print(f"Tangenta calculata cu numpy: {tan}")

    time_end_numpy = time.time()

    time_to_compute_numpy = time_end_numpy - time_start_numpy

    time_start_fractional = time.time()

    my_tan = aproximare_tan_fractii_continue(x, 1e-15)
    print(f"Tangenta aproximata prin fractii: {my_tan}")

    time_end_fractional = time.time()

    time_to_compute_fractional = time_end_fractional - time_start_fractional

    print("Time to compute fractional: ", time_to_compute_fractional, "\n")

    is_numpy_faster = time_to_compute_fractional > time_to_compute_numpy

    abs_value = abs(tan - my_tan)

    print(f"Diferenta: {abs_value}")
    print("The faster method of computing the tangent is numpy? ", is_numpy_faster, "\n" )

    return abs_value, time_to_compute_fractional

def run():
    o = sys.stdout

    poli_tan_error_counter = 0
    optimized_poli_tan_error_counter = 0
    faster_poli_tan_counter = 0

    # Redirect stdout to a file
    with open('output.txt', 'w') as f:
        sys.stdout = f

        i = 1
        while i <= 10:
            print("Iteration: ", i)

            x = random.uniform(10*(-1)*math.pi, 10*math.pi)

            print("This is the number: ", x)

            x = normalize_x(x)

            print("This is the number normalized: ", x, "\n")

            if math.isinf(x):
                print(f"The value of {x} is a multiple of pi/2, that means the tangent is infinite.")
                continue  # Skip this value to avoid crashing

            poli_tan_error, optimized_poli_tan_error, poli_tan_time = compare_polinomial_tan(x)
            frac_tan_error, frac_tan_time = compare_fraction_tan(x)

            if poli_tan_error > frac_tan_error:
                poli_tan_error_counter += 1

            if optimized_poli_tan_error > frac_tan_error:
                optimized_poli_tan_error_counter += 1

            if poli_tan_time < frac_tan_time:
                faster_poli_tan_counter += 1

            i = i + 1

    # Restore stdout
    sys.stdout = o

    print("The number of iterations is: ", i - 1, "\n")

    print("The number of times the polinomial method had a higher computing error than the fractional method is: ", poli_tan_error_counter)
    print("The number of times the fractional method had a higher computing error than the polinomial method is: ", i - poli_tan_error_counter - 1, "\n")

    print("The number of times the optimized polinomial method had a higher computing error than the fractional method is: ", optimized_poli_tan_error_counter)
    print("The number of times the fractional method had a higher computing error than the optimized polinomial method is: ", i - optimized_poli_tan_error_counter - 1, "\n")

    print("The number of times the polinomial method was faster than the fractional method is: ", faster_poli_tan_counter)
    print("The number of times the fractional method was faster than the polinomial method is: ",  i - faster_poli_tan_counter - 1, "\n")

print(run())