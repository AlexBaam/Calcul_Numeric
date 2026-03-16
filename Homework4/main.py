from pathlib import Path

def file_content(path):
    elements_count = -1 # fiindca avem un empty space la final incepem de la -1

    for file in path.iterdir():
        if file.is_file():
            f = open(file, 'r')
            elements_count += len(f.readlines())
            print("The number of elements in b_" + file.name + " is equal to: " + str(elements_count))

    print("")
    return elements_count

def nullity_check(path):
    epsilon = 1e-4

    for file in path.iterdir():
        if file.is_file():
            f = open(file, 'r')
            for i in f.readlines():
                # Aici am nevoie de niste sugestii findca aceasta castare la float(i) reduce precizia, de asta si numarul meu e asa mic pentru epsilon
                # Ar parea ca numerele cu o perioada foarte mare precum .6666666666666 sunt reduse la .66 indiferent de ce ar avea in urma perioadei, si nu stiu unde poate duce asta la calcule
                # Exista posibilitatea unor erori daca as avea numere precum 0.0001111111111111111134523 sau ceva, si atunci el nu ar fi nul, dar reducerea acestuia la un nr mai mic de zecimale
                # Il poate transforma intr-un 0.00 si atunci poate imi zice ca am element nul desi nu am, this is bs tbh
                if  i != '\n' and (abs(float(i) - epsilon) < epsilon): # Verific pe baza unei precizii faptul ca am elemente nule
                    print("There is an element in d0_" + file.name + " that is almost 0, that element is: " + str(i))
                    break

    print("There were no nule elements in d0 files")

def run():
    b_path = Path('b')
    d0_path = Path('d0')
    d1_path = Path('d1')
    d2_path = Path('d2')

    b_elements_count = file_content(b_path)
    d0_elements_count = file_content(d0_path)

    nullity_check(d0_path)

if __name__ == "__main__":
    run()