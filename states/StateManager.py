from states import StateMenu, StateAuthors, StateAuthors2


class StatesManager:
    states = {
        0: None,
        1: StateMenu,
        2: StateAuthors,
        3: StateAuthors2
    }

    @staticmethod
    def get_state(index):
        if index in StatesManager.states.keys():
            return StatesManager.states[index]
        else:
            return StatesManager.states[0]
