""""
    Just a simple vector code because i don`t want big amount of dependencies

"""


class Vector2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def scale(self, multiplier: float):
        self.x *= multiplier
        self.y *= multiplier

    def scale_to_new_vector(self, multiplier: float):
        return Vector2d(self.x * multiplier, self.y * multiplier)

    def normalize(self):
        self.scale(1 / abs(self))

    def __repr__(self):
        return f"{self.x} {self.y}"

    def __add__(self, other):
        return Vector2d(self.x + other.x, self.y + other.y)

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y

    def __sub__(self, other):
        return Vector2d(self.x - other.x, self.y - other.y)

    def __iadd__(self, other):
        self.x = self.x + other.x
        self.y = self.y + other.y
        return Vector2d(self.x, self.y)

    def __imul__(self, other):
        self.scale(self * other)
        return Vector2d(self.x, self.y)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return Vector2d(self.x, self.y)

    def clone(self):
        return Vector2d(self.x, self.y)

    def perp(self):
        """
        returns perpendicular vector

        """
        return Vector2d(self.x, -1 * self.y)
