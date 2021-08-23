class Output:
    def __init__(self, state) -> None:
        self.state = state

    def setState(self, newState):
        for key in newState:
            self.state[key] = newState[key]
        return self()
