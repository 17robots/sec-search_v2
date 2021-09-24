from typing import List, Callable, TypeVar, Any

T = TypeVar('T')

class Filter:
    def __init__(self, criteria: List[T], func: Callable[[T, List[T], bool], bool], inclusive: bool) -> None:
        self.criteria = criteria
        self.pass_func = func
        self.inclusive = inclusive
    def __call__(self, item) -> Any:
        return self.func(item, self.criteria, self.inclusive)