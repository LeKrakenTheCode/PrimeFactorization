from json import load, dump
from math import sqrt
from threading import Event, Thread
from os import path
from datetime import datetime
from functools import lru_cache

class PrimeFactorizer:
    """Class for Factorizing Number down to base factors (primes)"""
    primesFile = 'primes.json'
    primes = []
    maxValue = 0
    value = 0
    factors = []
    currentPrime = 2
    
    def __init__(self):
        self.loadPrimes()
    
    #@lru_cache()
    def isPrime(self, value):
        if value in self.primes:
            return True
        if value < 2 or value % 2 == 0:
            return False
        for odd in range(3, int(sqrt(value)) + 1, 2):
            if (value % odd == 0):
                return False
        return True
    
    #@lru_cache()
    def isPrimeList(self, value):
        if value in self.primes:
            return True
        self.maxValue = int(sqrt(value)) + 1
        if value < 2 or value % 2 == 0:
            return False
        for self.currentPrime in self.primes:
            if self.currentPrime > self.maxValue:
                return True
            if value % self.currentPrime == 0:
                return False
        return True

    
    def printPrimes(self):
        print('Prime List:')
        for prime in self.primes:
            print(prime)
    
    def progressReport(self, interval, func, *args):
        stopped = Event()
        def loop():
            while not stopped.wait(interval):
                func(*args)
        Thread(target=loop, daemon=True).start()
        return stopped.set
    
    def loadPrimes(self):
        if not path.exists(self.primesFile):
            open(self.primesFile, 'x', encoding='utf-8').close()
        with open(self.primesFile, 'r+') as f:
            try:
                f.seek(0)
                if (']' in f.read()):
                    f.seek(0)
                    self.primes = load(f)
                else:
                    print("Corrupted File. Attempting Fix...")
                    f.write(']')
                    f.flush()
                    f.seek(0)
                    self.primes = load(f)
            except Exception as e:
                print('Failed to read file', e)
        if (len(self.primes) < 3):
            self.primes = [2, 3, 5]
            self.dumpPrimes()
        self.primes.sort()
        print(f'Loaded %d Primes...' % len(self.primes))

    def dumpPrimes(self):
        with open(self.primesFile, 'w+', encoding='utf-8') as f:
            dump(self.primes, f, indent=1)
    
    def savePrimes(self):
        print("Saving Progress... ", end='')
        self.dumpPrimes()
        print("Done!")

    def printGeneratorProgress(self):
        print("Current: %3.2f%%, %d" % (self.value/self.maxValue*100.00, self.value))

    def printFactorizationProgress(self):
        print("Current: ", self.factors, self.value, self.currentPrime)

    def generatePrimes(self, _maxValue):
        self.maxValue = _maxValue
        progress = self.progressReport(10, self.printGeneratorProgress)
        autosave = self.progressReport(60, self.savePrimes)

        print('Generating Primes up to %d...' % self.maxValue)
        self.value = self.primes[-1] + 2
        while (self.value < self.maxValue):
            if self.isPrime(self.value):
                self.primes.append(self.value)        
            self.value += 2
            #print(str(num) + ' ', end='')
        self.primes.sort()
        self.dumpPrimes()
    
        progress()
        autosave()
    
foo = PrimeFactorizer()
now = datetime.now()
print(foo.isPrime(10043717723456414571))
print(datetime.now() - now)
