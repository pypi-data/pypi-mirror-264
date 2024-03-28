class MyString:
    """
    This module allows you to compare strings not by ord() values of chars, but by the length of the string - len()
    """

    def __init__(self, string: str) -> None:
        """
        string - your text
        """
        self.string = string

    def __eq__(self, other):
        return len(self.string) == len(other.string)

    def __gt__(self, other):
        return len(self.string) > len(other.string)

    def __ge__(self, other):
        return len(self.string) >= len(other.string)

    def __str__(self):
        return self.string

    def __repr__(self) -> str:
        return str(self)
