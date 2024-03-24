class Number:
    """
    A class to represent a number and check if it is odd or even.

    Attributes:
    - value (int): The value of the number.
    """

    def __init__(self, value):
        """
        Initialize a Number object with a given value.

        Parameters:
        - value (int): The value of the number.
        """
        self.value = value

    def is_even(self):
        """
        Check if the number is even.

        Returns:
        - str: 'Even' if the number is even, 'Odd' otherwise.
        """
        if self.value % 2 == 0:
            return 'Even'
        else:
            return 'Odd'
