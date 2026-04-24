from dataclasses import dataclass


@dataclass
class Commit:
    title: str
    author: str
    created_at: str
