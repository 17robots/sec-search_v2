from dataclasses import dataclass, field


@dataclass
class Event:
    type: str

# Search events


class InitSearchEvent(Event):
    type: field(default="InitSearchEvent")
