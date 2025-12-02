import os
from random import random

from DataStructures.Stack import Stack
from Design.Manager import Manager
from Design.User import User, Driver
from Interface.ManagerPage import ManagerPage
from Interface.UserPage import UserPage
from Repository.Handler import Handler


class LoginPage:
    def __init__(self,handler:Handler, stack : Stack) -> None :
        self.handler : Handler = handler
        self.stack : Stack = stack

    def showPage(self) :
        print("Login Page\n")
        print("0.Exit\n1.Login\n2.Register\n")
        try :
            inp : int = int(input("Enter your action : "))
            if inp == 0 :
                print("Goodbye. See you soon!")
                exit(0)
            if inp == 1 :
                username: int = int(input("\nEnter your username : "))
                password: str = input("Enter your password : ")
                manager : Manager | None = self.login_manager(username=username , password=password)
                if manager is None:
                    user : User | None = self.login_user(username=username , password=password)
                    if user is None:
                        print("Invalid username or password!\n")
                    else :
                        is_driver = False
                        searched_driver : Driver | None = None
                        for driver in self.handler.drivers:
                            if driver.id == user.id :
                                searched_driver = driver
                                is_driver = True
                                break
                        self.stack.push(UserPage(self.handler, user, is_driver, searched_driver,self.stack))
                else :
                    self.stack.push(ManagerPage(self.handler, manager, self.stack))
            elif inp == 2 :
                username: int = int(input("\nEnter your username : "))
                password: str = input("Enter your password : ")
                firstname: str = input("Enter your firstname : ")
                lastname: str = input("Enter your lastname : ")
                date_of_birth: str = input("Enter your date_of_birth : ")
                self.sign_up(username= username, firstname=firstname, lastname=lastname, date_of_birth=date_of_birth,
                             password=password)
            else:
                print("Invalid Input !")
        except Exception as e :
            print("Invalid Input !")

    def login_user(self, username: int, password: str) -> User | None:
        user = User("", "", username, password, "")
        existing_user: User | None = self.handler.users.search(user)
        if (existing_user is not None) and (existing_user.password == password):
            return existing_user
        else :
            return None

    def login_manager(self, username: int, password: str) -> Manager | None:
        if self.handler.manager.isValidLogin(username, password):
            return self.handler.manager
        else:
            return None

    def sign_up(self, username : int, firstname: str, lastname: str, date_of_birth: str, password: str) -> User | None:
        if len(password) != 8 or not User("", "", 0, "", "").has_letters_and_digits(password):
            print("Password must be 8 characters long and include both letters and digits.")
            return None

        user = User(firstname, lastname, username, password, date_of_birth)
        exists : User | None = self.handler.users.search(user)
        if (exists is not None) or (username == self.handler.manager.manager_id):
            print("This user already exists. Please try again!")
            return None

        self.handler.users.insert(user)

        with open(os.path.join(os.getcwd(), "InitialData", "users.txt"), "a", encoding="utf-8") as f:
            line = f"{user.id} | {user.firstname} | {user.lastname} | {user.date_of_birth} | {user.password}\n"
            f.write(line)

        return user







