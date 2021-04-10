from discord import Client, Activity, Status
from discord.ext.commands import Bot

from typing import Union, Callable, List

from time import time as get_time
from logging import getLogger, INFO, FileHandler, Logger
from asyncio import sleep

from discordex import extension
from discordex.permissions import Permissions


def _get_logger() -> Logger:
    logger: Logger = getLogger('discordex')
    logger.setLevel(INFO)
    logger.addHandler(FileHandler('discordex.log'))
    return logger


class Dex:
    """The Extension class

    Parameters
    ----------
    bot: Union[:class:`discord.Client`, :class:`discord.ext.commands.Bot`]
        The bot. Required
    logger: Optional[:class:`logging.Logger`]
        The logger for this module.
        You can customize this by sending a Logger object

    Attributes
    ----------
    bot: Union[:class:`discord.Client`, :class:`discord.ext.commands.Bot`]
        The discord bot
    extension: List[:class:`Extension`]
        The extension list
    logger: :class:`logging.Logger`
        The logger for this module
    """

    def __init__(self, bot: Union[Client, Bot], logger: Logger = _get_logger(), **kwargs):
        self.bot: Union[Client, Bot] = bot
        self.extensions: List['extension.Extension'] = []

        self._start_time: int = 0

        self.logger = logger

    async def change_presence_loop(self, *, presences: List[Union[Activity, Callable]], wait: int = 60, status: Status = Status.online, **kwargs) -> None:
        """Changes the presence every few seconds

        Parameters
        ----------
        presences: List[Union[:class:`discord.Activity`, :class:`Callable`]]
            The presence list
        wait: :class:`int`
            time to change the presence
        status: :class:`discord.Status`
            the bot's status
        """

        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            for _presence in presences:
                presence = _presence() if isinstance(_presence, Callable) else _presence
                await self.bot.change_presence(status=status, activity=presence, **kwargs)
                await sleep(wait)

    @property
    def uptime(self) -> Union[float, None]:
        """Union[:class:`float`, ``None``]: The uptime of the bot. ``None`` if the bot hasn't started
        """

        if not self._start_time:
            return None
        return get_time() - self._start_time

    def add(self, extension: 'extension.Extension', permissions: Permissions = Permissions()) -> 'extension.Extension':
        """Add the extension to the bot

        Parameters
        ----------
        extension: :class:`Extension`
            The extension
        permissions: :class:`Permissions`
            The extension's permissions
        """
        extension._attach_dex(self, self.bot)
        extension.permissions = permissions
        self.extensions.append(extension)
