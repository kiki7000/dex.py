from typing import Any
from ..context import Context


class BaseExtension:
    """Basic form of extension

    Every extensions should inherit this

    Parameters
    ----------
    name: str
        The extension's name. If not, the name of the class
    """

    def __init__(self, **kwargs):
        self.name = kwargs.get('name') or self.__name__

    async def before_execute(self, ctx: Context) -> None:
        """The function to run before excute

        If two or more extensions are added, they are executed in the order they were added

        :returns bool: executes the command if returns True

        Parameters
        ----------
        ctx: :class:`discordex.context.Context`
            the Context
        """
        pass

    async def after_execute(self, ctx: Context, returns: Any) -> None:
        """The function to run after excute

        If two or more extensions are added, they are executed in the order they were added

        Parameters
        ----------
        ctx: :class:`discordex.context.Context`
            the Context
        returns: Any
            the result returned by the pervious extension or the `execute` function. If returned none, None
        """
        pass
