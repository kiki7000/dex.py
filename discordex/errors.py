class DexException(Exception):
    """Base exception class for dex.py
    """
    pass


class BeforeCommandException(DexException):
    """Exception that's thrown before command processing
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
