from functools import lru_cache
import math, datetime

class PrimeFactorFinder():
    def __init__(self):
        self.__factors = []

    def timed(self, func):
        def wrapper(*args, **kwargs):
            now = datetime.datetime.now()
            parameters = ",".join(str(value) for value in args)
            print(f"{func.__name__}({parameters}) executing...")

            result = func(*args, **kwargs)

            time_diff = datetime.datetime.now() - now
            print(f"Complete: {time_diff}")
            return result
        return wrapper

    @lru_cache()
    def isPrime(self, number):
        maxFactor = int(math.sqrt(number))
        if number < 2 or number % 2 == 0:
            return False
        for odd in range(3, maxFactor, 2):
            if (number % odd == 0):
                return False
        return True
