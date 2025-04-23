from math import sqrt

def isPrime(number):
    if number == 2:
        return True
    elif number < 2 or number % 2 == 0:
        return False
    else:
        for factor in range(3, int(sqrt(number) + 1), 2):
            if number % factor == 0:
                return False
        return True

def factorize(number):
    if isPrime(number):
        return [1, number]
    else:
        factors = [1]
        startingNumber = number
        while number % 2 == 0:
            factors.append(2)
            number /= 2
        for factor in range(3, int(sqrt(startingNumber) + 1), 2):
            if isPrime(factor) and number != 1:
                while number % factor == 0:
                    number /= factor
                    factors.append(factor)
                    #print(number)
                if isPrime(number):
                    factors.append(int(number))
                    break
            if number == 1:
                break
        return factors
    
print(factorize(1267650600228229401496703205376))
print(factorize(20964422345233663458))