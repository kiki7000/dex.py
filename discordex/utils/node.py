from typing import Any
from json import load, dump


class Node(object):
    """Creates class attributes from dict

    Example

        >>> Node({'hello': 'kiki'}).hello
        kiki

    Parameters
    ----------
    dictionary: dict
        dictionary to convert into object
    """

    def __init__(self, dictionary: dict = {}):
        for key in dictionary:
            if not isinstance(key, str):
                continue
            val = dictionary[key]

            if not isinstance(val, dict):
                self[key] = val
            else:
                self[key] = Node(val)

        self._do = {
            "keys": lambda s: list(s.__dict__.keys()),
            "values": lambda s: list(s.__dict__.values()),
            "items": lambda s: list(s.__dict__.items()),
            "data": lambda s: s.__dict__,
        }

    def __getattr__(self, name: str) -> Any:
        if name in self._do:
            return self._do[name](self)
        if name not in self.__dict__:
            return None

        return self.__dict__[name]

    def __setattr__(self, name: str, value: Any) -> None:
        self.__dict__[name] = value

    def __getitem__(self, name: str) -> Any:
        if name in self._do:
            return self._do[name](self)
        if name not in self.__dict__:
            return None

        return self.__dict__[name]

    def __setitem__(self, name: str, value: Any) -> None:
        self.__dict__[name] = value

    def __delattr__(self, name: str) -> None:
        del self.__dict__[name]


class File(Node):
    """Open a file and turn it into Node class

    Example

        >>> File('config.json').hello # config.json is {'hello': 'kiki'}
        kiki

    Parameters
    ----------
    filePath: str
        the file's path
    encoding: str
        the file's encoding
    """

    def __init__(self, filePath: str, encoding: str = "utf-8", **kwargs):
        with open(filePath, "r", encoding="utf-8", **kwargs) as f:
            dictionary = load(f)
        super().__init__(dictionary)

        self.filePath = filePath

    def commit(self, encoding: str = "utf-8", ensure_ascii: bool = False, **kwargs) -> None:
        """Saves the data into the file

        Parameters
        ----------
        encoding: str
            the file's encoding
        """
        with open(self.filePath, "w", encoding=encoding) as f:
            dump(self.data, f, indent="\t", ensure_ascii=False)
