class MyString:
    def __init__(self, string):
        self.string = string

    def __eq__(self, other):
        return self.string == other.string

    def __gt__(self, other):
        return len(self.string) > len(other.string)

    def __ge__(self, other):
        return len(self.string) >= len(other.string)

    def __str__(self):
        return self.string

    def __repr__(self) -> str:
        return str(self)
