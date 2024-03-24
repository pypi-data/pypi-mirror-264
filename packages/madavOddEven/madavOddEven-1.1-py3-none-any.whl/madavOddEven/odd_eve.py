class Number:
    """
    A class to represent a number and check if it is odd or even.

    Attributes:
    - value (int): The value of the number.
    """


    def is_even(self,value):
        """
        Check if the number is even.

        Returns:
        - str: 'Even' if the number is even, 'Odd' otherwise.
        """
        if value % 2 == 0:
            return 'Even'
        else:
            return 'Odd'
