import random


class Manager:
    def __init__(self , manager_id : int , password : str):
        self.manager_id = manager_id
        self.key = chr(random.randint(1, 200))
        self.password: str = password

    def isValidLogin(self, manager_id : int ,password : str) -> bool:
        return manager_id == self.manager_id and password == self.password


