from CryptographyLib import util


def constructZn(n):
    ans = []
    for i in range(1, n):
        if util.binaryGCD(n, i) == 1:
            ans.append(i)
    return ans


if __name__ == "__main__":
    while True:
        try:
            print(constructZn(int(input())))
        except Exception as e:
            print(e)
