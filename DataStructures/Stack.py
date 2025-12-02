from DataStructures.LinkedList import LinkedList


class Stack:
    def __init__(self):
        self.items = LinkedList()

    def is_empty(self):
        return not self.items.head

    def push(self, item):
        self.items.insert_at_tail(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.remove_from_tail()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self.items.tail
