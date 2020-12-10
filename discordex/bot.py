from discord import AutoShardedClient, User, Status, Game, Activity, Message
from asyncio import sleep
from typing import List, Callable, Union, Optional
from time import time as get_time
from re import sub
from functools import wraps
from inspect import isclass

from .context import Context
from .base import BaseExtension, BaseCommand
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
    """

    _blacklist: List[int] = []
    _whitelist: List[int] = []
    _ownerlist: List[int] = []

    _allow_bots: bool = False
    _allow_privates: bool = True

    _extensions: List[BaseExtension] = []

    _start_time: int = 0

    def __init__(self, command_prefix: str, **kwargs):
        self.command_prefix = command_prefix.strip(' ')

        self.blacklist = kwargs.get('blacklist')
        self.whitelist = kwargs.get('whitelist')
        self.ownerlist = kwargs.get('ownerlist')

        self._allow_bots = kwargs.get('allow_bots')
        self._allow_privates = kwargs.get('allow_privates')
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

    def command(self, main_cmd: str, aliases: List[str] = [], **kwargs) -> Callable:
        """
        Decorate version or :func:`add_command`
        """

        def decorate(cmd: Union[BaseCommand, Callable]) -> Union[BaseCommand, Callable]:
            self.add_command(cmd, main_cmd, aliases, **kwargs)
            return cmd

        return decorate

    def add_command(self, cmd: Union[BaseCommand, Callable], main_cmd: str, aliases: List[str] = [], **kwargs) -> Union[BaseCommand, Callable]:
        """
        Initialize the command and append the command into the list

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
        """
        for cmd_string in aliases + [main_cmd]:
            if isclass(cmd):
                self.cmds.add(cmd_string, cmd(self, **kwargs))
            else:
                self.cmds.add(cmd_string, cmd)

        return cmd

    async def on_message(self, message: Message) -> None:
        """:func:`process_cmd`'s alias
        """

        await self.process_cmd(message)
        return None

    async def process_cmd(self, message: Message) -> Optional[Message]:
        if message.author.id in self.blacklist:
            return

        if self.whitelist and message.author.id not in self.whitelist:
            return

        if message.author.bot and not self._allow_bots:
            return

        if str(message.channel.type) != 'text' and not self._allow_privates:
            return

        parsed_content = self.parse_content(message.content)

        ctx = Context()
        ctx.cmd = parsed_content.cmd
        ctx.args = parsed_content.args

        ctx.message = message
        ctx.content = message.content
        ctx.bot = self

        ctx.channel = message.channel
        ctx.author = message.author
        ctx.guild = message.guild

        ctx.send = message.channel.send

        cmd = self.cmds.search(message.content)
        if not cmd:
            return None
        ctx.command = cmd[1]
        cmd_string = cmd[0]

        ctx.nargs = self.cmds.get_nargs(message, cmd_string)

        if callable(ctx.command):
            await ctx.command(ctx)
        else:
            await ctx.command.use_command(ctx)
        return message

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
