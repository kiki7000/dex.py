from discord import Client
from discord.ext.commands import Bot

from typing import Union, Optional

from discordex import dex
from discordex.permissions import Permissions


class Extension:
    """The extension class

    .. note::
        Every extensions should inherit this class

    Attributes
    ----------
    bot: :class:`Optional[Union[discord.Client, discord.ext.commands.Bot]]`
        The bot

    dex: :class:`Optional[discordex.Dex]`
        The dex client
    """

    def __init__(self, **kwargs):
        self.bot: Optional[Union[Client, Bot]] = None
        self.dex: Optional["dex.Dex"] = None

        self._permissions: Permissions = Permissions()

    @property
    def permissions(self) -> Permissions:
        """
        The extension's permissions
        """
        return self._permissions

    @permissions.setter
    def permissions(self, value: Permissions):
        if isinstance(value, Permissions):
            self._permissions = value

    def on_load(self):
        """Executed when the extension is added

        .. note::
            In default, it prints a LOG
        """
        self.dex.logger.info("Exension loaded")
        pass

    def _attach_dex(self, dex: "dex.Dex", bot: Union[Client, Bot]):
        self.dex = dex
        self.bot = bot
        self.on_load()
