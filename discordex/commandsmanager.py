from typing import Deque, Union, Iterable
from collections import deque
from discord import AutoShardedClient
from re import compile, MULTILINE

from .base import BaseCommand


class CommandsManager:
    """Commands Manager

    Parameters
    ----------
    bot: :class:`discordex.DexBot`
        The bot class

    Attributes
    ----------
    bot: :class:`discordex.DexBot`
        The bot class
    """

    _cmds: Deque[BaseCommand] = deque([])

    def __init__(self, bot: AutoShardedClient):
        self.bot = bot

    def _get_typestr_regex(self, type: str, compiled: bool = False) -> str:
        string = f'<{type}:[a-zA-Z][a-zA-Z1-9]*>'
        return string if not compiled else compile(string)

    def cmd_string_content_match(self, content: str, cmd_string: str) -> bool:
        """Check if the content matches the cmd_string
        :returns bool: Whether the message content matches the cmd_string

        Parameters
        ----------
        content: :class:`str`
            Message content
        cmd_string: :class:`str`
            The cmd string
        """

        def check_int(string: str) -> bool:
            try:
                int(string)
            except ValueError:
                return False
            else:
                return True

        stringtypelist = {
            'str': lambda _: True,
            'int': check_int,
            'user': lambda mention: compile('<@!\\d{16,}>').match(mention) and self.bot.get_user(mention[3:-1]),
            'channel': lambda mention: compile('<#\\d{16,}>').match(mention) and self.bot.get_channel(mention[2:-1]),
            'role': lambda mention: compile('<@&\\d{16,}>').match(mention),
            'url': lambda url: compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)').match(url),
            'longstr': lambda _: True
        }

        parsed_cmd_string = self.bot.parse_content(cmd_string, False)
        parsed_content = self.bot.parse_content(content)

        if parsed_content.cmd != parsed_cmd_string.cmd or parsed_cmd_string.args.count(self._get_typestr_regex('longstr')) > 1:
            return False
        if self._get_typestr_regex('longstr') in parsed_cmd_string.args and parsed_cmd_string.args[-1] != self._get_typestr_regex('longstr'):
            return False

        for _i in range(len(parsed_cmd_string.args)):
            arg = parsed_cmd_string.args[_i]

            if _i == len(parsed_cmd_string.args) - 1:
                regex = compile(f'{"|".join(map(self._get_typestr_regex, stringtypelist.keys()))}')
            else:
                regex = compile(f'{"|".join(map(self._get_typestr_regex, stringtypelist.keys()[:-1]))}')

            if not regex.match(arg):
                return False

            try:
                type = arg[1:].split(':')[0]
                varname = arg[2 + len(type): -1]
            except IndexError:
                return False

            if not stringtypelist[type](arg):
                return False

        return True

    def search(self, content: str) -> Union[BaseCommand, None]:
        """Searches the command by message content
        :returns: the command (if none was found, None)

        Parameters
        ----------
        content: :class:`str`
            Message content
        """

        content = content.lower().strip()

        for cmd in self._cmds:
            if self.cmd_string_content_match(content, cmd.main_cmd) or len(filter(lambda alias: self.cmd_string_content_match(content, alias), cmd.aliases_cmd)) > 0:
                return cmd

        return None

    def add(self, command: BaseCommand) -> BaseCommand:
        """Adds the command into the list
        :returns: the command to add

        Parameters
        ----------
        command: :class:`.base.BaseCommand`
            The command to add

        Raises
        ------
        :exc:`TypeError`
            Command didn't inherit BaseCommand
        """

        if not isinstance(command, BaseCommand):
            raise TypeError('Command should inherit BaseCommand')

        if command in self._cmds:
            return command

        self._cmds.append(command)
        return command

    def __len__(self) -> int:
        return len(self._cmds)

    def __list__(self) -> list:
        return self._cmds

    def __iter__(self) -> Iterable:
        return self._cmds
