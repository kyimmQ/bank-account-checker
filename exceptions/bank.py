class CannotFoundAccount(Exception):
    pass

class AccountNotMatch(Exception):
    def __init__(self, account:str, msg: str):
        self.account = account
        super().__init__(msg)