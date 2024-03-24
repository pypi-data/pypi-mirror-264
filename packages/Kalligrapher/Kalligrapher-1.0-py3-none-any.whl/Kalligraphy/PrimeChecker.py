class PrimeChecker:
    """
    A class to check whether a given number is prime.

    Attributes:
        number (int): The number to check for primality.
    """


    def is_prime(self, value):
        """
        Checks if the number is prime.

        Returns:
            bool: True if the number is prime, False otherwise.
        """
        if self.number <= 1:
            return False

        for divisor in range(2, int(self.number**0.5) + 1):
            if self.number % divisor == 0:
                return False

        return True


