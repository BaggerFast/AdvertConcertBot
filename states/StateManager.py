from misc import StateIndex
from states import StateMenu, StateAuthors, StateAuthors2


class StatesManager:
    states = {
        StateIndex.default: None,
        StateIndex.menu: StateMenu,
        StateIndex.authors: StateAuthors,
        StateIndex.authors2: StateAuthors2
    }

    @staticmethod
    def get_state(index):
        if index in StatesManager.states.keys():
            return StatesManager.states[index]
        else:
            return StatesManager.states[0]
