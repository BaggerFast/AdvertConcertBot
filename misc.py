import dataclasses


@dataclasses.dataclass
class EventInfo:
    message: dict
    user_id: int
    command: str
