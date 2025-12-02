from typing import TypeVar, Generic, Optional, Callable

from DataStructures.LinkedList import LinkedList

T = TypeVar('T')


class AVLNode(Generic[T]):
    def __init__(self, key: T):
        self.key: T = key
        self.left: Optional['AVLNode[T]'] = None
        self.right: Optional['AVLNode[T]'] = None
        self.height: int = 1


class AVLTree(Generic[T]):
    def __init__(self, key_func: Callable[[T], any] = lambda x: x):
        self.root: Optional[AVLNode[T]] = None
        self.key_func = key_func

    def _height(self, node: Optional[AVLNode[T]]) -> int:
        return node.height if node else 0

    def _update_height(self, node: AVLNode[T]) -> None:
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node: AVLNode[T]) -> int:
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, y: AVLNode[T]) -> AVLNode[T]:
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x: AVLNode[T]) -> AVLNode[T]:
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self._update_height(x)
        self._update_height(y)
        return y

    def _balance(self, node: AVLNode[T]) -> AVLNode[T]:
        self._update_height(node)
        balance = self._balance_factor(node)

        # Left heavy
        if balance > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right heavy
        if balance < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _insert(self, node: Optional[AVLNode[T]], key: T) -> AVLNode[T]:
        if not node:
            return AVLNode(key)
        if self.key_func(key) < self.key_func(node.key):
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)
        return self._balance(node)

    def insert(self, key: T) -> None:
        self.root = self._insert(self.root, key)

    def _min_value_node(self, node: AVLNode[T]) -> AVLNode[T]:
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _delete(self, node: Optional[AVLNode[T]], key: T) -> Optional[AVLNode[T]]:
        if not node:
            return None
        if self.key_func(key) < self.key_func(node.key):
            node.left = self._delete(node.left, key)
        elif self.key_func(key) > self.key_func(node.key):
            node.right = self._delete(node.right, key)
        else:
            if not node.left or not node.right:
                return node.left or node.right
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)
        return self._balance(node) if node else None

    def delete(self, key: T) -> None:
        self.root = self._delete(self.root, key)

    def _search(self, node: Optional[AVLNode[T]], key: T) -> T | None:
        if not node:
            return None
        if self.key_func(key) == self.key_func(node.key):
            return node.key
        elif self.key_func(key) < self.key_func(node.key):
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def search(self, key: T) -> T | None:
        return self._search(self.root, key)

    def _inorder(self, node: Optional[AVLNode[T]], linked_list: LinkedList[T]) -> None:
        if node:
            self._inorder(node.left, linked_list)
            linked_list.insert_at_tail(node.key)
            self._inorder(node.right, linked_list)

    def inorder(self) -> LinkedList[T]:
        linked_list = LinkedList[T]()
        self._inorder(self.root, linked_list)
        return linked_list

    def _inorder_generator(self, node: Optional[AVLNode[T]]):
        if node:
            yield from self._inorder_generator(node.left)
            yield node.key
            yield from self._inorder_generator(node.right)

    def __iter__(self):
        return self._inorder_generator(self.root)