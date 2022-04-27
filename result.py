from dataclasses import dataclass


@dataclass(frozen=True)
class Result:
    id: str
    level: str
    object_names: tuple[str]
