from discord import AutoShardedClient

from traceback import print_exc
from typing import Any, List

from ..context import Context
from .extension import BaseExtension


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
    extensions: List[:class:`.BaseExtension`]
        The extensions

    main_cmd: :class:`str`
        The command form
    aliases_cmd: List[:class:`str`]
        Aliases of the cmd

    guild_cooltime: int
        The cooltime of the guild (default 0)
    channel_cooltime: int
        The cooltime of the channel (default 0)
    user_cooltime: int
        The cooltime of the user (default 0)
    """

    def __init__(self, bot: AutoShardedClient):
        self.bot = bot

        self.extensions: BaseExtension = []

        self.main_cmd: str = None
        self.aliases_cmd: List[str] = []

        self.guild_cooltime: int = 0
        self.channel_cooltime: int = 0
        self.user_cooltime: int = 0

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
