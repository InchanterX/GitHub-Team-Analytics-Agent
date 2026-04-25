from dataclasses import dataclass


@dataclass
class Commit:
    sha: str
    author: str
    message: str
    date: str
    verified: bool = False
    files_changed: int = 0
