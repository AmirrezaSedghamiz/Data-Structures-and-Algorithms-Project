from typing import TypeVar, Generic, Optional, Callable

T = TypeVar('T')


class Node(Generic[T]):
    def __init__(self, data: T):
        self.data: T = data
        self.next: Optional['Node[T]'] = None


class LinkedList(Generic[T]):
    def __init__(self, equals_func: Callable[[T, T], bool] = lambda a, b: a == b):
        self.head: Optional[Node[T]] = None
        self.tail: Optional[Node[T]] = None
        self.equals_func = equals_func
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def insert_at_head(self, data: T) -> None:
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self._size += 1

    def insert_at_tail(self, data: T) -> None:
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def search(self, data: T) -> T | None:
        current = self.head
        while current:
            if self.equals_func(current.data, data):
                return current.data
            current = current.next
        return None

    def delete(self, data: T) -> bool:
        current = self.head
        prev = None
        while current:
            if self.equals_func(current.data, data):
                if prev is None:
                    self.head = current.next
                    if self.head is None:
                        self.tail = None
                else:
                    prev.next = current.next
                    if current.next is None:
                        self.tail = prev
                self._size -= 1
                return True
            prev = current
            current = current.next
        return False

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

    def remove_from_head(self) -> Optional[T]:
        if self.head is None:
            return None
        data = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self._size -= 1
        return data

    def remove_from_tail(self) -> Optional[T]:
        if self.head is None:
            return None
        if self.head == self.tail:
            data = self.head.data
            self.head = None
            self.tail = None
            self._size = 0
            return data

        current = self.head
        while current.next != self.tail:
            current = current.next

        data = self.tail.data
        current.next = None
        self.tail = current
        self._size -= 1
        return data