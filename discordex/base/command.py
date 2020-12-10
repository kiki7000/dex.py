from discord import AutoShardedClient

from traceback import print_exc
from typing import Any, List

from .extension import BaseExtension


class BaseCommand:
    """Basic form of command

    Every command should inherit this

    Parameters
    ----------
    bot: :class:`discordex.DexBot`
        The bot class

    main_cmd: :class:`str`
        The command form
    aliases: List[:class:`str`]
        Aliases of the cmd

    guild_cooltime: int
        The cooltime of the guild (default 0)
    channel_cooltime: int
        The cooltime of the channel (default 0)
    user_cooltime: int
        The cooltime of the user (default 0)
    role_cooltime: int
        The cooltime of the role (default 0)

    Attributes
    ----------
    bot: :class:`discordex.DexBot`
        The bot class

    guild_cooltime: int
        The cooltime of the guild (default 0)
    channel_cooltime: int
        The cooltime of the channel (default 0)
    user_cooltime: int
        The cooltime of the user (default 0)
    role_cooltime: int
        The cooltime of the role (default 0)
    """

    def __init__(self, bot: AutoShardedClient, guild_cooltime: int = 0, channel_cooltime: int = 0, user_cooltime: int = 0, role_cooltime: int = 0):
        self.bot = bot

        self._extensions: List[BaseExtension] = []

        self.guild_cooltime: int = 0
        self.channel_cooltime: int = 0
        self.user_cooltime: int = 0
        self.role_cooltime: int = 0

    def use(self, ext: BaseException) -> BaseException:
        self.extensions.append(ext)
        return ext

    async def before_execute(self, ctx) -> bool:
        """The function to run before excute

        This function is executed before other extensions

        :returns bool: executes the command if returns True

        Parameters
        ----------
        ctx: :class:`discordex.context.Context`
            the Context
        """
        pass

    async def execute(self, ctx) -> Any:
        """The execute function

        This function is executed before other extensions

        :returns: Result to send to after_execute function (default None)

        Parameters
        ----------
        ctx: :class:`discordex.context.Context`
            the Context
        """
        pass

    async def after_execute(self, ctx, returns: Any) -> None:
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

    async def error_handler(self, ctx, ex: Exception) -> None:
        """Function executed when an ERRrOR occurs while executing

        Parameters
        ----------
        ctx: :class:`discordex.context.Context`
            the Context
        ex: :class:`Extension`
            Exception raised during execution
        """
        print_exc()

    async def use_command(self, ctx) -> None:
        """The function that runs the extension, executes

        .. warning::
            You can customize this but the problem caused by customizing this can't be solved

        Parameters
        ----------
        ctx: :class:`discordex.context.Context`
            the Context
        """

        do = True
        do = (await self.before_execute(ctx)) in (None, True)
        for ext in self.extensions:
            if not do:
                return
            do = (await ext.before_execute(ctx)) in (None, True)
        if not do:
            return

        try:
            returns = await self.execute(ctx)
        except Exception as e:
            await self.error_handler(ctx, e)
            if self.bot.base_errorhandler:
                await self.bot.base_errorhandler(ctx, e)

        await self.after_execute(ctx, returns)
        for ext in self.extensions:
            await ext.after_execute(ctx, returns)

    @property
    def extensions(self) -> List[BaseExtension]:
        """
        The extensions of the command
        """
        return self._extensions

    @extensions.setter
    def extensions(self, value):
        self._extensions = value
