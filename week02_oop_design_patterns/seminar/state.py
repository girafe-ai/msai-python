from collections import defaultdict
from dataclasses import dataclass


class StateEvents:
    MOUSEMOVE = 'mousemove'
    BALANCE_CHANGE = 'balance_change'


class StateMachine:
    def __init__(self):
        self.handlers = defaultdict(list)

    def bind(self, event_name: str, handler: callable):
        self.handlers[event_name].append(handler)

    def unbind(self, event_name: str, handler: callable):
        pass

    def trigger(self, event_name, *args, **kwargs):
        for handler in self.handlers[event_name]:
            handler(*args, **kwargs)


@dataclass
class State:
    mouse_coordinates: list
    balance: float
    buttons: Button

    _state_machine: StateMachine

    def move_the_mouse(self, new_coords):
        self._state_machine.trigger(StateEvents.MOUSEMOVE)

    def change_balance(self, new_balance):
        pass

    def press_button(self, button):
        pass

    def release_button(self, button):
        pass


