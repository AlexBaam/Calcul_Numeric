from pathlib import Path

def file_content(path):
    elements_count = {}

    for file in path.iterdir():
        if file.is_file():
            f = open(file, 'r')
            current_count = len(f.readlines()) - 1 # fiindca avem un empty space la final incepem de la -1
            f.close()

            elements_count[file.name] = current_count
            print("The number of elements in " + path.name + "_" + file.name + " is equal to: " + str(current_count))

    print("")
    return elements_count

def nullity_check(path):
    epsilon = 1e-4
    found_null = False

    for file in path.iterdir():
        if file.is_file():
            f = open(file, 'r')
            for i in f.readlines():
                # Aici am nevoie de niste sugestii findca aceasta castare la float(i) reduce precizia, de asta si numarul meu e asa mic pentru epsilon
                # Ar parea ca numerele cu o perioada foarte mare precum .6666666666666 sunt reduse la .66 indiferent de ce ar avea in urma perioadei, si nu stiu unde poate duce asta la calcule
                # Exista posibilitatea unor erori daca as avea numere precum 0.0001111111111111111134523 sau ceva, si atunci el nu ar fi nul, dar reducerea acestuia la un nr mai mic de zecimale
                # Il poate transforma intr-un 0.00 si atunci poate imi zice ca am element nul desi nu am, this is bs tbh
                if  i != '\n' and (abs(float(i)) < epsilon): # Verific pe baza unei precizii faptul ca am elemente nule
                    print("There is an element in d0_" + file.name + " that is almost 0, that element is: " + str(i))
                    found_null = True
                    break

    if not found_null:
        print("There were no nule elements in d0 files")

def diagonals_number(d0_elements_count, d1_elements_count, d2_elements_count):
    for file_name in d0_elements_count:
        if file_name in d1_elements_count and file_name in d2_elements_count:
            p = d0_elements_count[file_name] - d1_elements_count[file_name]
            q = d0_elements_count[file_name] - d2_elements_count[file_name]

            print("For file " + file_name + " we have: p = " + str(p) + ", q = " + str(q))
        else:
            print("File " + file_name + " is missing from d1 or d2")

def run():
    b_path = Path('b')
    d0_path = Path('d0')
    d1_path = Path('d1')
    d2_path = Path('d2')

    b_elements_count = file_content(b_path)
    d0_elements_count = file_content(d0_path)
    d1_elements_count = file_content(d1_path)
    d2_elements_count = file_content(d2_path)

    for file_name in b_elements_count:
        if file_name in d0_elements_count:
            if b_elements_count[file_name] != d0_elements_count[file_name]:
                print(
                    "The number of elements in b_" + file_name + " and d0_" + file_name + " is not equal, cannot solve the system")
        else:
            print("File " + file_name + " exists in b but not in d0")

    nullity_check(d0_path)

    diagonals_number(d0_elements_count, d1_elements_count, d2_elements_count)

if __name__ == "__main__":
    run()