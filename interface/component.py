
class Component:
    def __init__(self, props=None) -> None:
        self.param = props
        self.state = {}

    def render(): pass

    def setState(self, newState):
        for key in newState:
            self.state[key] = newState[key]
        return self()
    
    def __call__(self):
        return self.render()