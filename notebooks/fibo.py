def fibo(n):
    if n <= 1:
        return 1
    return fibo(n-1) + fibo(n-2)

def main():
    import sys
    print(fibo(int(sys.argv[1])))

main()