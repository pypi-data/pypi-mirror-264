from __future__ import annotations
from typing import Any, Callable


class Monad:

    def __init__(self, value: Any):
        self.value = value

    def get(self) -> Any:
        return self.value

    def or_else(self, func: Callable[[Any], Any]) -> Any:
        return func(self.value)

    def map(self, func: Callable[[Any], Any]) -> Monad:
        return Monad(func(self.value))

    def map_or(self, func1: Callable[[Any], Any], func2: Callable[[Any], Any]) -> Monad:
        return Monad(func1(self.value))

    def flatmap(self, func: Callable[[Any], Monad]) -> Monad:
        return func(self.value)
    
    def flatmap_or(self, func1: Callable[[Any], Monad], func2: Callable[[Any], Monad]) -> Monad:
        return func1(self.value)

    def __eq__(self, other):
        if not isinstance(other, Monad):
            return NotImplemented
        return type(self) == type(other) and self.value == other.value

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"


class Option(Monad):

    @staticmethod
    def maybe(value):
        return SomeOption(value) if value else NoneOption(value)


class SomeOption(Option):

    def or_else(self, _: Callable[[Any], Any]) -> Any:
        return self.value

    def map(self, func) -> Monad:
        return Option.maybe(func(self.value))

    def map_or(self, func: Callable[[Any], Any], _) -> Monad:
        return Option.maybe(func(self.value))



class NoneOption(Option):
    
    def __init__(self, value: Any = None):
        self.value = value
    
    def or_else(self, func: Callable[[Any], Any]) -> Any:
        return func(self.value)

    def map(self, _) -> Monad:
        return self

    def map_or(self, _, func: Callable[[Any], Any]) -> Monad:
        return self

    def flatmap(self, _) -> Monad:
        return self
    
    def flatmap_or(self, _, func: Callable[[Any], Any]) -> Monad:
        return func(self.value)


class Stateable:

    def enter(self) -> Stateable:
        raise NotImplementedError

    def leave(self) -> Stateable:
        raise NotImplementedError

    def update(self) -> Monad:
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError
