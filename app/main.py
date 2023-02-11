from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int = None, max_amount: int = None) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: str, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, obj: str, value: int) -> None:
        return getattr(obj, self.protected_name)

    def __set__(self, obj: str, value: int) -> (None, bool):
        if value in range(self.min_amount, self.max_amount + 1):
            setattr(obj, self.protected_name, value)
        else:
            return False


class Visitor:

    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self,
                 age: int,
                 height: int,
                 weight: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height
        self.has_access = False


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def __init__(self, age: int, height: int, weight: int) -> None:
        super().__init__(age, height, weight)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(self, age: int, height: int, weight: int) -> None:
        super().__init__(age, height, weight)


class Slide:
    def __init__(self,
                 name: str,
                 limitation_class: (ChildrenSlideLimitationValidator,
                                    AdultSlideLimitationValidator)) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        age = visitor.age
        height = visitor.height
        weight = visitor.weight
        slide = self.limitation_class(age, height, weight)
        if len(slide.__dict__) < 4:
            return False
        return True
