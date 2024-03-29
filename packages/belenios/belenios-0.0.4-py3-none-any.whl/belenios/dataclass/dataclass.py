from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class KeysPair:
    public_key: int
    private_key: int


@dataclass
class Group:
    description: str
    p: int
    g: int
    q: int
@dataclass
class EncryptedText:
    chunk: List[Tuple[int, int]] # (u, v)
@dataclass
class EncryptedTextAndK:
    chunk: List[Tuple[int, int, int]] # ( u, v, k )


@dataclass
class PrivateCredential:
    index: int
    private_credential: str
    email: str
