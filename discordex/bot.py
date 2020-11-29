from discord import AutoShardedClient, User, Status, Game, Activity
from asyncio import sleep
from typing import List, Callable, Union
from time import time as get_time


class DexBot(AutoShardedClient):
    r"""The Bot class

    Parameters
    ----------
    command_prefix: str
        the bot's prefix. None if none given
    """

    _blackList: List[User] = []

    _start_time: int = 0

    def __init__(self, command_prefix: str = None, **kwargs):
        self.command_prefix = command_prefix
        super().__init__(**kwargs)

    def run(self, token: str, *args, **kwargs) -> None:
        """Starts the bot

        Parameters
        ----------
        token: str
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
        wait: int
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

    @property
    def uptime(self) -> Union[float, None]:
        """Union[:class:`float`, ``None``]: The uptime of the bot. ``None`` if the bot hasn't started
        """

        if not self._start_time:
            return None
        return get_time() - self._start_time

    @property
    def blackList(self):
        """List[:class:`discord.User`]: The bot's blacklist. If the black listed user uses the command, it raises the :class:`discordex.errors.BlacklistedUser`
        """
        return self._blackList

    @blackList.setter
    def blackList(self, value: List[User]):
        self._blackList = value
