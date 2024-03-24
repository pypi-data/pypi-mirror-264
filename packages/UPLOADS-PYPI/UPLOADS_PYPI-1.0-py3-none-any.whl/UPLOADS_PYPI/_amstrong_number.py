class ArmstrongNumber:
    """
    A class representing an Armstrong number and providing a method to check if a number is Armstrong or not.
    """


    def is_armstrong(self,value):
        """
        Check if the number is an Armstrong number.

        Returns:
        bool: True if the number is an Armstrong number, False otherwise.
        """
        num_str = str(value.number)
        num_digits = len(num_str)
        armstrong_sum = sum(int(digit) ** num_digits for digit in num_str)
        return armstrong_sum == value.number