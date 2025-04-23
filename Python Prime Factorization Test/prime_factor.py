import json, math, os, datetime
from functools import lru_cache
#from datetime import datetime

class primeChecker:
    primesFile = 'primes.json'
    primes = []

    def __init__(self):
            
            self.loadPrimes()

    def printPrimes(self):
        print('Prime List:')
        for prime in self.primes:
            print(prime)

    def loadPrimes(self):
        if not os.path.exists(self.primesFile):
            open(self.primesFile, 'x').close()
        with open(self.primesFile, 'r+') as f:
            try:
                f.seek(0)
                if (']' in f.read()):
                    f.seek(0)
                    self.primes = json.load(f)
                else:
                    print("Corrupted File. Attempting Fix...")
                    f.write(']')
                    f.flush()
                    f.seek(0)
                    self.primes = json.load(f)
            except Exception as e:
                print('Failed to read file', e)
        if (len(self.primes) < 3):
            self.primes = [2, 3, 5]
            self.dumpPrimes()
        self.primes.sort()
        print('Loaded %d Primes...' % len(self.primes))

    def dumpPrimes(self):
        with open(self.primesFile, 'w+') as f:
            json.dump(self.primes, f, indent=1)

    def generatePrimes(self, maxValue):
        autosave = datetime.datetime.now()
        update = autosave
        print('Generating Primes up to %d...' % maxValue)
        num = self.primes[-1] + 2
        while (num < maxValue):
            if self.isPrime(num):
                self.primes.append(num)
                now = datetime.datetime.now()
                if now - update >= datetime.timedelta(seconds=10):
                    print("Current: %3.2f%%, %d" % (num/maxValue*100.00, num))
                    update = now

                if datetime.datetime.now() - autosave >= datetime.timedelta(seconds=60):
                    print("Saving Progress... ", end='')
                    self.dumpPrimes()
                    autosave = now
                    print("Done!")
            num += 2
            #print(str(num) + ' ', end='')
        self.primes.sort()
        self.dumpPrimes()

    @lru_cache()
    def isPrime(self, value):
        if (int(value) in self.primes):
            return True
        maxFactor = int(math.sqrt(value))
        if value < 2 or value % 2 == 0:
            return False
        for odd in range(3, maxFactor, 2):
            if (value % odd == 0):
                return False
        return True

    def factorLoop(self, value, startingIndex = 0):
        originalValue = int(value)
        update = datetime.datetime.now()
        now = update
        maxFactor = int(math.sqrt(value))
        factors = []
        result = 1
        
        for prime in self.primes[startingIndex:]:
            if prime > maxFactor or int(value) in self.primes or int(result) == originalValue or int(value) == 1:
                break
            now = datetime.datetime.now()
            while (int(value) > 1 and int(value) % prime == 0):
                value /= prime
                result *= int(prime)
                factors.append(int(prime))
                if self.isPrime(value):
                    result *= value
                    factors.append(int(value))
                    value = 1
            if now - update >= datetime.timedelta(seconds=10):
                print("Current: ", factors, value, prime)
                update = now
        
        return factors, value, result == originalValue
    
    def factorize(self, value):
        originalValue = int(value)
        
        print('Factorizing %d...' % value)
        if not self.isPrime(value):
            
            factors, value, result = self.factorLoop(value)

            if (value != 1 and (input('Need to generate more primes to solve. Proceed? [y/n] >')).upper() == 'Y'):
                prevPrime = len(self.primes) - 1
                self.generatePrimes(int(math.sqrt(value)))
                print('Refactoring with additional primes:')
                _factors, value, result = self.factorLoop(value, prevPrime)
                factors.extend(_factors)
                    

            print('Factors: ')
            result = 1
            mergedFactors = self.mergeFactors(factors)

            print('(1)', end='')
            for factor in mergedFactors:
                result *= factor ** mergedFactors[factor]
                if mergedFactors[factor] != 1:
                    print('*(%d^%d)' % (factor, mergedFactors[factor]), end='')
                else:
                    print('*(%d)' % (factor), end='')
                
                print('=%d' % result)
                if result == originalValue:
                    print('Confirmed Factors!')
                    return mergedFactors
                else:
                    print('Something Went Wrong')
                    return -1
        else:
            print("Value is Prime")
            return {value: 1}
        
            
    def mergeFactors(self, factors):
        mergedFactors = {}
        for factor in factors:
            if factor in mergedFactors:
                mergedFactors[factor] += 1
            else:
                mergedFactors[factor] = 1
        return mergedFactors

foo = primeChecker()
#foo.factorize(1267650600228229401496703205376)
#foo.factorize(20964422345233663458)
now = datetime.datetime.now()
foo.factorize(126765060022822912341234401496703205376)
print(datetime.datetime.now() - now)
