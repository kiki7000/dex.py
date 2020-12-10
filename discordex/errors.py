class DexException(Exception):
    """Base exception class for dex.py
    """
    pass


class BlackListedUser(BeforeCommandException):
    """Exception that's thrown when a blacklisted user uses the bot
    """
    pass


class NotWhiteListedUser(BeforeCommandException):
    """Exception that's thrown when a not whitelisted user uses the bot (Only when whitelist is enabled)
    """
    pass


class UserisBot(BeforeCommandException):
    """Exception that's thrown when a bot uses the command
    """
    pass


class PrivateChannel(BeforeCommandException):
    """Exception that's thrown when the command is not used at text channel
    """
    pass
