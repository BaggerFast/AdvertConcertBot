from misc.addition import StateIndex
from states import StateMenu, StateAuthors, StateAuthors2


class StatesManager:
    states = {
        StateIndex.default: None,
        StateIndex.menu: StateMenu,
        StateIndex.authors: StateAuthors,
        StateIndex.state_manager: StateAuthors2
    }

    @staticmethod
    def get_state(index: int):
        return StatesManager.states[index] if index in StatesManager.states.keys() else StatesManager.states[0]

