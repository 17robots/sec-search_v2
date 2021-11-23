class SuperClient:
    def __init__(self, client_type: str, accts=None, regs=None) -> None:
        if client_type == "ec2":
            return EC2Client(accts, regs)
        elif client_type == "logs":
            return LogClient(accts, regs)
            ...
        else:
            raise Exception("Invalid Client Type")

    def __new__(cls: Type[_T]) -> _T:
      ...


  class EC@Client(SuperClient)