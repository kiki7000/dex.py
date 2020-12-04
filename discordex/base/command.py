from discord import AutoShardedClient

from traceback import print_exc
from typing import Any

from ..context import Context


class BaseCommand:
    """Basic form of command

    Every command should inherit this

    Parameters
    ----------
    bot: :class:`discordex.DexBot`
        The bot class

    Attributes
    ----------
    bot: :class:`discordex.DexBot`
        The bot class
    """

    def __init__(self, bot: AutoShardedClient):
        self.bot = bot

    async def before_execute(self, ctx: Context) -> None:
        """The function to run before excute

        This function is executed before other extensions

        :returns bool: executes the command if returns True

        Parameters
        ----------
        ctx: :class:`discordex.context.Context`
            the Context
        """
        pass

    async def execute(self, ctx: Context) -> None:
        """The execute function

        This function is executed before other extensions

        :returns: Result to send to after_execute function (default None)

        Parameters
        ----------
        ctx: :class:`discordex.context.Context`
            the Context
        """
        pass

    async def after_execute(self, ctx: Context, returns: Any) -> None:
        """The function to run after excute

        This function is executed before other extensions

        Parameters
        ----------
        ctx: :class:`discordex.context.Context`
            the Context
        returns: Any
            the result returned by the `execute` function returned. If returned none, None
        """
        pass

    async def error_handler(self, ctx: Context, ex: Exception):
        """Function executed when an ERRrOR occurs

        Parameters
        ----------
        ctx: :class:`discordex.context.Context`
            the Context
        ex: :class:`Extension`
            Exception raised during execution
        """
        print_exc()
