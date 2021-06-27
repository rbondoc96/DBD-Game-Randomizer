class AssetNotFound(Exception):
    code = "AssetNotFound"

class MultipleInstancesOfUniqueAsset(Exception):
    code = "MultipleInstancesOfUniqueAsset"

class PlayerNameTooLong(Exception):
    code = "PlayerNameTooLong"

class NoPlayerWithMatchingId(Exception):
    code = "NoPlayerWithMatchingId"

class HostIsNotKiller(Exception):
    code = "HostIsNotKiller"

class KillerIsNotHost(Exception):
    code = "KillerIsNotHost"

class NoHostIdGiven(Exception):
    code = "NoHostIdGiven"

class NoSessionIdGiven(Exception):
    code = "NoSessionIdGiven"

class SessionIsFull(Exception):
    code = "SessionIsFull"

class NoSessionWithMatchingId(Exception):
    code = "NoSessionWithMatchingId"

class UnsupportedSessionMode(Exception):
    code = "UnsupportedSessionMode"

class UnableToCreateSession(Exception):
    code = "UnableToCreateSession"


class ErrorTypes:
    AssetNotFound = AssetNotFound
    MultipleInstancesOfUniqueAsset = MultipleInstancesOfUniqueAsset

    PlayerNameTooLong = PlayerNameTooLong
    NoPlayerWithMatchingId = NoPlayerWithMatchingId

    HostIsNotKiller = HostIsNotKiller
    KillerIsNotHost = KillerIsNotHost
    NoHostIdGiven = NoHostIdGiven
    NoSessionIdGiven = NoSessionIdGiven
    SessionIsFull = SessionIsFull
    NoSessionWithMatchingId = NoSessionWithMatchingId
    UnsupportedSessionMode = UnsupportedSessionMode
    UnableToCreateSession = UnableToCreateSession