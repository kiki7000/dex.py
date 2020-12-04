from typing import TypeVar

T = TypeVar('T', bound='Collection')


class Collection:
    def __init__(self, lst: list):
        self.array = lst
