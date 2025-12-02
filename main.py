from Interface.LoginPage import LoginPage
from DataStructures.Stack import Stack
from Repository.Handler import Handler


def navigator(navigationStack: Stack, myHandler: Handler):
    while True:
        navigationStack.peek().data.showPage()


if __name__ == '__main__':
    handler : Handler = Handler()
    handler.initialize()
    stack : Stack = Stack()
    stack.push(LoginPage(handler, stack))
    navigator(stack, handler)


