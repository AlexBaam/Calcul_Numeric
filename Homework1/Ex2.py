from Ex1 import find_u
import random

def asociativitate_adunare():

    u = find_u()
    x = 1.0
    y = u/10
    z = y

    print(f"x: {x}\n  y: {y}\n  z: {z}\n")

    left_side =  (x + y) + z
    right_side = x + (y + z)

    print(f"left_side: {left_side}\n right_side: {right_side}\n")

    if left_side != right_side:
        return f"ex2: adunarea nu este asociativa\n"

print(asociativitate_adunare())

def asociativitate_inmultire():
    while True:
        x = random.random()
        y = random.random()
        z = random.random()

        print(f"x: {x}\n  y: {y}\n  z: {z}\n")

        left_side = (x * y) * z
        right_side = x * (y * z)

        print(f"left_side: {left_side}\n  right_side: {right_side}\n")

        if left_side != right_side:
            return f"ex2: inmultirea nu este asociativa\n"

print(asociativitate_inmultire())