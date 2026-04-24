from dataclasses import dataclass


@dataclass
class Issue:
    title: str
    author: str
    created_at: str
