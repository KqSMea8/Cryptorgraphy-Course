from exp1_3 import congruenceEquation

if __name__ == "__main__":
    while True:
        k = input().split()
        if len(k) <= 1:
            print("Usage: ", __file__ + " a, n")
        t = congruenceEquation(int(k[0]), 1, int(k[1]))
        if len(t) == 0:
            print("No Solution")
        else:
            print(t)
