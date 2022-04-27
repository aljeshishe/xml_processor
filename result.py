from dataclasses import dataclass


@dataclass(frozen=True)
class Result:
    id: str
    level: int
    object_names: tuple[str]
