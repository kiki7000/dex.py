class DexException(Exception):
    """Base exception class for dex.py
    """
    pass


class BeforeCommandException(DexException):
    """Exception that's thrown before command processing
    """
    pass


class BlacklistedUser(BeforeCommandException):
    """Exception that's thrown when a blacklisted user uses the bot
    """
    pass
