from dataclasses import dataclass, field
from queue import Queue


@dataclass
class Event:
    e_type: str


class MessagePump:
    def __init__(self) -> None:
        self.messagePump: Queue = Queue()
        self.listeners = {}

    def addListener(self, type, callback):
        self.listeners[type] = callback

    def processEvents(self):
        if self.messagePump.qsize() == 0:
            return
        event = self.messagePump.get(block=False)
        if event.e_type in self.listeners:
            self.listeners[event.e_type](event)
