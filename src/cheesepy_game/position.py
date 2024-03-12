
class Position():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def to_tuple(self):
        return (self.x, self.y)

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __str__(self) -> str:
        return f"(x:{self.x}, y:{self.y})"

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def times(self, v: int):
        p = Position(*self.to_tuple())
        p.x *= v
        p.y *= v
        return p

    def add_scalar(self, v: int):
        p = Position(*self.to_tuple())
        p.x += v
        p.y += v
        return p
