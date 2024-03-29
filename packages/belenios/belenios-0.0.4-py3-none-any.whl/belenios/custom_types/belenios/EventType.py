from enum import Enum


class EventType(Enum):
    Setup = 'Setup'
    Ballot = 'Ballot'
    EndBallots = 'EndBallots'
    EncryptedTally = 'EncryptedTally'
    Shuffle = 'Shuffle'
    EndShuffles = 'EndShuffles'
    PartialDecryption = 'PartialDecryption'
    Result = 'Result'
