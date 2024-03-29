class ITDEError(Exception):
    """ """


class KeyNotFound(ITDEError, KeyError):
    """ """


class EndpointNotFound(ITDEError):
    """ """


class UnexpectedState(ITDEError):
    """ """


class UnregisteredElement(ITDEError):
    """ """


class UnregisteredHeaderType(UnregisteredElement):
    """ """


class UnregisteredItemType(UnregisteredElement):
    """ """
