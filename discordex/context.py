from discord import Message, AutoShardedClient
from typing import List, Union

from .utils import Node
from .base import BaseCommand


class Context(Node):
    cmd: str
    args: List[str]

    message: Message
    content: str
    bot: AutoShardedClient

    command: BaseCommand
    cmd_string: str

    nargs: Node

    def __init__(self):
        super().__init__({})
