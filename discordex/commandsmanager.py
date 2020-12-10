from typing import Union, Iterable, Dict, Callable, Tuple, Optional, List
from discord import AutoShardedClient, Message
from re import compile, MULTILINE

from .base import BaseCommand
from .utils import Node


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

    _cmds: Dict[str, BaseCommand] = {}

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

        varnames = []

        for _i in range(len(parsed_cmd_string.args)):
            if _i == len(parsed_cmd_string.args) - 1:
                regex = compile(f'{"|".join(map(self._get_typestr_regex, stringtypelist.keys()))}')
            else:
                regex = compile(f'{"|".join(map(self._get_typestr_regex, list(stringtypelist.keys())[:-1]))}')

            arg = parsed_cmd_string.args[_i]
            string_type = regex.match(arg)

            if not string_type:
                return False

            try:
                _type = arg[1:].split(':')[0]
                varname = arg[2 + len(_type): -1]
            except IndexError:
                return False

            if _type == 'longstr':
                contarg = ' '.join(parsed_content.args[_i:])
            else:
                contarg = parsed_content.args[_i]

            if not stringtypelist[_type](contarg):
                return False

            if varname in varnames:
                return False
            varnames.append(varname)

        return True

    def get_nargs(self, message: Message, cmd_string: str) -> Union[Node, bool]:
        """Get the nargs
        :returns: The nargs (False if the cmd_string doesn't matches the content)

        Parameters
        ----------
        message: :class:`discord.Message`
            The message
        cmd_string: :class:`str`
            The cmd string
        """

        action = {
            'user': lambda string: self.bot.get_user(int(string)),
            'channel': lambda string: self.bot.get_channel(int(string)),
            'role': lambda string: message.guild.get_role(int(string))
        }

        content = message.content
        if not self.cmd_string_content_match(content, cmd_string):
            return False

        res = Node()

        parsed_cmd_string = self.bot.parse_content(cmd_string, False)
        parsed_content = self.bot.parse_content(content)

        for _i in range(len(parsed_cmd_string.args)):
            arg = parsed_cmd_string.args[_i]
            _type = arg[1:].split(':')[0]
            varname = arg[2 + len(_type): -1]

            if _type == 'longstr':
                contarg = ' '.join(parsed_content.args[_i:])
            else:
                contarg = parsed_content.args[_i]

            if _type in action:
                res[varname] = action[_type](contarg)
            else:
                res[varname] = contarg

        return res

    def search(self, content: str) -> Optional[Tuple[str, Union[BaseCommand, Callable]]]:
        """Searches the command by message content
        :returns tuple: the command string and command (if none was found, None)

        Parameters
        ----------
        content: :class:`str`
            Message content
        """

        content = content.lower().strip()

        for cmd_string in self._cmds:
            if self.cmd_string_content_match(content, cmd_string):
                return cmd_string, self._cmds[cmd_string]

        return None

    def add(self, cmd_string: str, command: Union[BaseCommand, Callable]) -> Union[BaseCommand, Callable]:
        """Adds the command into the list
        :returns: the command to add

        Parameters
        ----------
        command: Union[:class:`.base.BaseCommand`, Callable]
            The command to add

        Raises
        ------
        :exc:`TypeError`
            Command didn't inherit BaseCommand (if Command is class)
        """

        if not callable(command) and not isinstance(command, BaseCommand):
            raise TypeError('Command should inherit BaseCommand')

        self._cmds[cmd_string] = command
        return command

    def __dict__(self) -> int:
        return self._cmds

    def __iter__(self) -> Iterable[str]:
        return iter(self._cmds.keys())

    def __str__(self) -> str:
        return str(self._cmds)
