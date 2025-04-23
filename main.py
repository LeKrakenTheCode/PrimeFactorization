from primefactorfinder import *
import random

def main():
    foo = PrimeFactorFinder()
    for x in range(1000):
        print(foo.timed(foo.isPrime)(random.randint(2, 9999999999999999999999)))
    #print(foo.timed(foo.isPrime)(6735249118018991))
    #print(foo.isPrime(6735249118018991))
    #print(foo.timed_isPrime(1559144712891223110910871021929883839727659613569547479457389367277233211975331))


main()