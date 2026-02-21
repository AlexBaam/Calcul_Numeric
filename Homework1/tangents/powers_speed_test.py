from math import pi
import random
import time

def rand_x():

    lower_bound = (pi / 2) * (-1)
    upper_bound = (pi / 2)

    print("This is lower_bound: ", lower_bound)
    print("This is upper_bound: ", upper_bound)

    x = random.uniform(lower_bound, upper_bound)

    print("This is the number: ", x)

    return x

def pow_test():
    start_time = time.time()

    x = rand_x()

    print("3rd power: ", pow(x,3))
    print("5th power: ", pow(x,5))
    print("7th power: ", pow(x,7))
    print("9th power: ", pow(x,9))

    end_time = time.time()

    elapsed_time = end_time - start_time

    print("Elapsed time: ", elapsed_time)

def manual_pow_test():
    start_time = time.time()

    x = rand_x()

    x_2nd = x * x
    x_3rd = x_2nd * x
    x_5th = x_3rd * x_2nd
    x_7th = x_5th * x_2nd
    x_9th = x_7th * x_2nd

    print("x_2nd: ", x_2nd)
    print("x_3rd: ", x_3rd)
    print("x_5th: ", x_5th)
    print("x_7th: ", x_7th)
    print("x_9th: ", x_9th)

    end_time = time.time()

    elapsed_time = end_time - start_time

    print("Elapsed time: ", elapsed_time)

print(pow_test())
print(manual_pow_test())