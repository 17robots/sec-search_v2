class Test:
    def __init__(self) -> None:
        self.item1 = "Hello"
        self.item2 = "World"
        for item in vars(self):
            print(getattr(self, item))


test = Test()
