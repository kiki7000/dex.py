from discord import AutoShardedClient, User, Status, Game, Activity
from asyncio import sleep
from typing import List, Callable, Union
from time import time as get_time
from re import sub

from .base import BaseExtension
from .commandsmanager import CommandsManager
from .utils import Node


class DexBot(AutoShardedClient):
    """The Bot class

    Parameters
    ----------
    command_prefix: str
        the bot's prefix. None if none given

    blacklist: List[:class:`int`]
        the IDs of users in the blacklist

    whitelist: List[:class:`int`]
        the IDs of users in the whitelist

    ownerlist: List[:class:`int`]
        the IDs of users in the ownerlist

    allow_bots: :class:`bool`
        Allow bots using the bot

    allow_privates: :class:`bool`
        Allow private channels

    space_after_prefix: :class:`bool`
        If there is a space after prefix
    """

    _blacklist: List[int] = []
    _whitelist: List[int] = []
    _ownerlist: List[int] = []

    _allow_bots: bool = False
    _allow_privates: bool = True
    _space_after_prefix: bool = False

    _extensions: List[BaseExtension] = []

    _start_time: int = 0

    def __init__(self, command_prefix: str, **kwargs):
        self.command_prefix = command_prefix.strip(' ')

        self.blacklist = kwargs.get('blacklist')
        self.whitelist = kwargs.get('whitelist')
        self.ownerlist = kwargs.get('ownerlist')

        self._allow_bots = kwargs.get('allow_bots')
        self._allow_privates = kwargs.get('allow_privates')
        self._space_after_prefix = kwargs.get('space_after_prefix')
        super().__init__(**kwargs)

        self.cmds = CommandsManager(self)

    def run(self, token: str, *args, **kwargs) -> None:
        """Starts the bot

        Parameters
        ----------
        token: :class:`str`
            The bot's token
        """

        self._start_time = get_time()
        super().run(token, *args, **kwargs)

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

        await self.wait_until_ready()

        while not self.is_closed():
            for _presence in presences:
                presence = _presence() if isinstance(_presence, Callable) else _presence
                await self.change_presence(status=status, activity=presence, **kwargs)
                await sleep(wait)

    def parse_content(self, content: str, include_prefix: bool = True) -> Node:
        """Parse the message content

        Parameters
        ----------
        content: :class:`str`
            Message Content
        include_prefix: :class:`bool`
            Whether the message content includes a prefix
        """

        content = sub(r' +', ' ', (content[len(self.command_prefix):].strip(' ') if include_prefix else content.strip(' ')))
        cmd = content.split()[0].lower()

        try:
            args = content[len(cmd) + 1:].split()
        except IndexError:
            args = []

        return Node({
            'cmd': cmd,
            'args': args
        })

    @property
    def uptime(self) -> Union[float, None]:
        """Union[:class:`float`, ``None``]: The uptime of the bot. ``None`` if the bot hasn't started
        """

        if not self._start_time:
            return None
        return get_time() - self._start_time

    @property
    def blacklist(self):
        """List[:class:`int`]:
            The bot's blacklist

            If the black listed user uses the command, it raises the :class:`discordex.errors.BlackListedUser`
        """
        return self._blacklist

    @blacklist.setter
    def blacklist(self, value: List[int]):
        self._blacklist = value

    @property
    def whitelist(self):
        """List[:class:`int`]:
            The bot's whitelist

            If the not whitelisted user uses the command, it raises the :class:`discordex.errors.NotWhiteListedUser` (Only when whitelist is enabled)
        """
        return self._whitelist

    @whitelist.setter
    def whitelist(self, value: List[int]):
        self._whitelist = value

    @property
    def ownerlist(self, value: List[int]):
        """List[:class:`int`]: The bot's ownerlist. Does nothing
        """
        return self._ownerlist

    @ownerlist.setter
    def ownerlist(self, value: List[int]):
        self._ownerlist = value
