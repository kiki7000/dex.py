class DexException(Exception):
    """Base exception class for dex.py
    """
    pass


class BlackListedUser:
    """Exception that's thrown when a blacklisted user uses the bot
    """
    pass


class NotWhiteListedUser:
    """Exception that's thrown when a not whitelisted user uses the bot (Only when whitelist is enabled)
    """
    pass


class UserisBot:
    """Exception that's thrown when a bot uses the command
    """
    pass


class PrivateChannel:
    """Exception that's thrown when the command is not used at text channel
    """
    pass
