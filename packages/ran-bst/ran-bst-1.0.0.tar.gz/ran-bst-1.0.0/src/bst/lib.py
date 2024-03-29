"""
Binary Search Tree Implementation

Author: Ran (01-ERFA)
Date created: 26/03/2024
Last modified: 28/03/2024

This module contains the implementation of a binary search tree (BST).
"""
from collections import deque

class BinaryNode:
    def __init__(self, value, son0 = None, son1 = None) -> None:
        self.__value = value
        self.__son0  = son0
        self.__son1  = son1

    @staticmethod
    def __is(other):
        return isinstance(other, BinaryNode)

    def __lt__(self, other):
        return self.__is(other) and self.__value <  other.__value

    def __eq__(self, other):
        return self.__is(other) and self.__value == other.__value

    def __gt__(self, other):
        return self.__is(other) and self.__value >  other.__value

    def get(self):
        return self.__value
    def set(self, value):
        self.__value = value

    def son0(self):
        return self.__son0
    def son1(self):
        return self.__son1

    def set0(self, value):
        assert self.__is(value) or isinstance(value, type(None)), f" '{type(value)}' is not a node"
        self.__son0 = value

    def set1(self, value):
        assert self.__is(value) or isinstance(value, type(None)), f" '{type(value)}' is not a node"
        self.__son1 = value

class BinarySearchTree:
    """
    Represents a binary search tree (BST) capable of storing elements of a specified type.

    Usage:
        bst = BinarySearchTree(int)

    Parameters:
        type: The type of elements to be stored in the binary search tree. It should support comparison
        operators such as ">" (greater than), "<" (less than), and "==" (equal to). Once the type is defined,
        the binary search tree can only work with elements of that type.

    Raises:
        TypeError: If the specified type does not support the required comparison operators.

    Attributes:
        __root: The root node of the binary search tree.
        __size: The number of elements in the binary search tree.
        __type: The type of elements stored in the binary search tree.

    Methods:
        add(element): Adds a new element to the binary search tree.
        remove(element): Removes the specified element from the binary search tree.
        inorder(): Returns a list containing the elements of the binary search tree in sorted order (in-order traversal).
        preorder(): Returns a list containing the elements of the binary search tree in pre-order traversal order.
        postorder(): Returns a list containing the elements of the binary search tree in post-order traversal order.
        levelorder(): Returns a list containing the elements of the binary search tree in level-order traversal order.
        spiralorder(): Returns a list containing the elements of the binary search tree in spiral order.
        height(): Returns the height of the binary search tree.
        stabilize(): Balances the binary search tree to improve efficiency.
        size(): Returns the number of elements in the binary search tree.
        min(): Returns the minimum element in the binary search tree.
        max(): Returns the maximum element in the binary search tree.
        pop(): Removes and returns the maximum element from the binary search tree.
        popleft(): Removes and returns the minimum element from the binary search tree.
        get(index=0): Returns the element at the specified index (default: 0) in sorted order.
        exist(value): Checks if the specified value exists in the binary search tree.
        copy(): Returns a deep copy of the binary search tree.

        __repr__(): Returns a string representation of the binary search tree.
        __len__(): Returns the number of elements in the binary search tree.
        __iter__(): Returns an iterator for the binary search tree.
        __add__(other): Concatenates two binary search trees or appends an element of the tree's type to the tree.
        __radd__(other): Concatenates two binary search trees or appends an element of the tree's type to the tree (reversed).
        __sub__(other): Removes elements from the binary search tree based on another binary search tree or removes a single element if present.
        __contains__(other): Checks if a value exists in the binary search tree or checks if a binary search tree is contained within another binary search tree.
        __eq__(other): Checks if the binary search tree is equal to another binary search tree.
        __getitem__(index): Returns the element at the specified index in sorted order.

    """

    def __init__(self, bst_type) -> None:
        self.__root = None
        self.__size = 0
        self.__type = bst_type
        
    def __repr__(self) -> str:
        """
        Returns a string representation of the binary search tree.

        Returns:
            A string representation of the binary search tree.
        """
        return f"BST({self.__type.__name__}):{repr(self.preorder())}"
    
    def __len__(self) -> int: 
        """
        Returns the number of elements in the binary search tree.

        Returns:
            The number of elements in the binary search tree as an integer.
        """
        return self.size()
    
    def __iter__(self):
        """
        Returns an iterator for the binary search tree.

        Returns:
            An iterator for the binary search tree.
        """
        yield from self.inorder()

    def __add__(self, other):
        """
        Concatenates two binary search trees or appends an element of the tree's type to the tree.

        Parameters:
            other: Another binary search tree or an element of the tree's type.

        Returns:
            A new binary search tree containing the elements of both trees or the original tree with the appended element.

        Raises:
            TypeError: If the specified type of 'other' is not compatible with the type of elements in the binary search tree.
        """
        bst = self.copy()

        if isinstance(other, BinarySearchTree):
            for node in other.preorder(): bst.add(node)
        elif isinstance(other, self.__type): bst.add(other)
        else: raise TypeError(f"unsupported operand type(s) for +: '{BinarySearchTree.__name__}({self.__type.__name__})' and '{other.__class__.__name__}'")

        return bst
    
    def __radd__(self, other):
        """
        Concatenates two binary search trees or appends an element of the tree's type to the tree (reversed).

        Parameters:
            other: Another binary search tree or an element of the tree's type.

        Returns:
            A new binary search tree containing the elements of both trees or the original tree with the appended element.

        Raises:
            TypeError: If the specified type of 'other' is not compatible with the type of elements in the binary search tree.
        """
        return self.__add__(other)
    
    def __sub__(self, other):
        """
        Removes elements from the binary search tree based on another binary search tree or removes a single element if present.

        Parameters:
            other: Another binary search tree or an element of the tree's type.

        Returns:
            A new binary search tree with elements removed based on the specified 'other' object.

        Raises:
            TypeError: If the specified type of 'other' is not compatible with the type of elements in the binary search tree.
        """
        bst = self.copy()

        if isinstance(other, BinarySearchTree):
            for node in other.preorder(): bst.remove(node)
        elif isinstance(other, self.__type): bst.remove(other)
        else: raise TypeError(f"unsupported operand type(s) for -: '{BinarySearchTree.__name__}({self.__type.__name__})' and '{other.__class__.__name__}'")

        return bst
    
    def __contains__(self, other) -> bool:
        """
        Checks if a value exists in the binary search tree or checks if a binary search tree is contained within another binary search tree.

        Parameters:
            other: Another binary search tree or a value of the tree's type to search for.

        Returns:
            True if the specified value exists in the binary search tree or if the binary search tree 'other' is contained within the current binary search tree, False otherwise.

        Raises:
            TypeError: If the specified type of 'other' is not compatible with the type of elements in the binary search tree.
        """
        if not isinstance(other, BinarySearchTree): return self.exist(other)
        return all(self.exist(val) for val in other.inorder())
    
    def __eq__(self, other) -> bool: 
        """
        Checks if the binary search tree is equal to another binary search tree.

        Parameters:
            other: Another binary search tree to compare with.

        Returns:
            True if the binary search tree is equal to the 'other' binary search tree, False otherwise.

        Raises:
            TypeError: If the specified type of 'other' is not compatible with the type of elements in the binary search tree.
        """
        return isinstance(other, BinarySearchTree) and self in other and other in self
    
    def __getitem__(self, index):
        """
        Returns the element at the specified index in the sorted order of the binary search tree.

        Parameters:
            index (int): The index of the element to retrieve.

        Returns:
            The element at the specified index in the sorted order of the binary search tree.

        Raises:
            IndexError: If the index is out of range.
        """
        try: return self.inorder()[index]
        except IndexError: raise IndexError("index out of range")

    def stabilize(self) -> None:
        """
        Balances the binary search tree to improve efficiency.
        """
        inorder_nodes = self.inorder()
        if not inorder_nodes: return
        
        m = len(inorder_nodes) // 2
        self.__root = BinaryNode(inorder_nodes[m])

        stack = [(self.__root, 0, inorder_nodes[m+1:]), (self.__root, 1, inorder_nodes[:m])]

        while stack:
            parent, son, nodes = stack.pop()
            if not nodes: continue

            m = len(nodes) // 2
            node = BinaryNode(nodes[m])

            if bool(son): parent.set0(node)
            else: parent.set1(node)
            
            stack.append((node, 0, nodes[m+1:]))
            stack.append((node, 1, nodes[:m]))

    def add(self, value) -> bool:
        """
        Adds a new element to the binary search tree.

        Parameters:
            element: The element to be added to the binary search tree.

        Returns:
            bool: True if the value is successfully added, False otherwise.
            
        Raises:
            TypeError: If the 'value' is not of the same type as the elements stored in the binary search tree.

        """
        if not isinstance(value, self.__type): raise TypeError (f"expected an '{self.__type.__name__}', but received a '{type(value).__name__}'")

        insert = BinaryNode(value)
        if not isinstance(self.__root, BinaryNode): self.__root = insert; self.__size+=1; return True;

        current = self.__root
        while isinstance(current, BinaryNode):
            if insert < current: 
                if not isinstance(current.son0(), BinaryNode):
                    current.set0(insert)
                    self.__size+=1
                    return True
                else: current = current.son0();
            elif insert > current:
                if not isinstance(current.son1(), BinaryNode):
                    current.set1(insert)
                    self.__size+=1
                    return True
                else: current = current.son1()
            else: return False;
        return False

    def remove(self, value) -> bool:
        """
        Removes the specified element from the binary search tree.

        Parameters:
            element: The element to be removed from the binary search tree.

        Returns:
            bool: True if the value is successfully removed, False if the value is not found in the binary search tree.
        
        Raises:
            TypeError: If the 'value' is not of the same type as the elements stored in the binary search tree.
        """
        if not isinstance(value, self.__type): raise TypeError (f"expected an '{self.__type.__name__}', but received a '{type(value).__name__}'")
        if not isinstance(self.__root, BinaryNode): return False

        current_node = self.__root
        parent       = None
        remove_node  = BinaryNode(value)
        
        while isinstance(current_node, BinaryNode):
            if remove_node < current_node:
                parent = current_node
                current_node = current_node.son0()
            elif remove_node > current_node:
                parent = current_node
                current_node = current_node.son1()
            else:
                if not isinstance(current_node.son0(), BinaryNode) or not isinstance(current_node.son1(), BinaryNode):
                    if not isinstance(current_node.son0(), BinaryNode):
                        next_node = current_node.son1()
                    else: next_node = current_node.son0()

                    if isinstance(parent, BinaryNode):
                        if parent.son0() == current_node: parent.set0(next_node)
                        else: parent.set1(next_node)
                    else: self.__root = next_node
                    # self.__size-=1
                    # return True
                else:
                    succesor = current_node.son1()
                    succesor_parent = current_node

                    while isinstance(succesor.son0(), BinaryNode):
                        succesor_parent = succesor
                        succesor = succesor.son0()
                    
                    current_node.set(succesor.get())

                    if succesor_parent.son0() == succesor: succesor_parent.set0(succesor.son1())
                    else: succesor_parent.set1(succesor.son1())
                self.__size-=1
                return True
        
        return False
        
    def size(self) -> int:
        """
        Returns the number of elements in the binary search tree.

        Returns:
            The number of elements in the binary search tree as an integer.
        """ 
        return self.__size

    def inorder(self) -> list:
        """
        Returns a list containing the elements of the binary search tree in sorted order (in-order traversal).

        Returns:
            A list containing the elements of the binary search tree in sorted order.
        """
        if not isinstance(self.__root, BinaryNode): return []

        nodes   = []
        stack   = []
        current = self.__root

        while True:
            if isinstance(current, BinaryNode):
                stack.append(current)
                current = current.son0()
            elif stack:
                current = stack.pop()
                nodes.append(current.get())
                current = current.son1()
            else:
                break;
        return nodes
    
    def preorder(self) -> list:
        """
        Returns a list containing the elements of the binary search tree in pre-order traversal order.

        Returns:
            A list containing the elements of the binary search tree in pre-order traversal order.
        """
        if not isinstance(self.__root, BinaryNode): return []

        nodes   = []
        stack   = [self.__root]

        while stack:
            current = stack.pop()
            nodes.append(current.get())

            if isinstance(current.son1(), BinaryNode):
                stack.append(current.son1())

            if isinstance(current.son0(), BinaryNode):
                stack.append(current.son0())
            
        return nodes

    def postorder(self) -> list:
        """
        Returns a list containing the elements of the binary search tree in post-order traversal order.

        Returns:
            A list containing the elements of the binary search tree in post-order traversal order.
        """
        if not self.__root: return []

        nodes = []
        stack = [self.__root]

        while stack:
            current = stack.pop()
            nodes.append(current.get())

            if current.son0():
                stack.append(current.son0())

            if current.son1():
                stack.append(current.son1())

        return nodes[::-1]

    def min(self):
        """
        Returns the minimum element in the binary search tree.

        Returns:
            The minimum element in the binary search tree.
            If the binary search tree is empty, return None.
        """
        if not isinstance(self.__root, BinaryNode): return None;

        current = self.__root
        while isinstance(current.son0(), BinaryNode): current = current.son0()

        return current.get()
    
    def max(self):
        """
        Returns the maximum element in the binary search tree.

        Returns:
            The maximum element in the binary search tree.
            If the binary search tree is empty, return None.
        """
        if not isinstance(self.__root, BinaryNode): return None;
        
        current = self.__root
        while isinstance(current.son1(), BinaryNode): current = current.son1()
        
        return current.get()

    def popleft(self):
        """
        Removes and returns the minimum element from the binary search tree.

        Returns:
            The minimum element in the binary search tree.
            If the binary search tree is empty, return None.
        """
        if not isinstance(self.__root, BinaryNode): return None;

        current = self.__root
        last    = None
        while isinstance(current.son0(), BinaryNode):
            last    = current
            current = current.son0()
        
        res = current.get()
        if isinstance(last, BinaryNode): last.set0(current.son1())
        else: self.__root = current.son1()
        self.__size-=1
        return res
    
    def pop(self):
        """
        Removes and returns the maximum element from the binary search tree.

        Returns:
            The maximum element in the binary search tree.  
            If the binary search tree is empty, return None.
        """
        if not isinstance(self.__root, BinaryNode): return None;

        current = self.__root
        last    = None
        while isinstance(current.son1(), BinaryNode):
            last    = current
            current = current.son1()
        
        res = current.get()
        if isinstance(last, BinaryNode): last.set1(current.son0())
        else: self.__root = current.son0()
        self.__size-=1
        return res

    def height(self) -> int:
        """
        Returns the height of the binary search tree.

        Returns:
            The height of the binary search tree as an integer.
        """
        if not isinstance(self.__root, BinaryNode): return 0;

        queue = deque([(self.__root, 1)])
        max_height = 0

        while queue:
            node, level = queue.popleft()
            max_height  = max(max_height, level)

            if isinstance(node.son0(), BinaryNode): queue.append((node.son0(), level+1))
            if isinstance(node.son1(), BinaryNode): queue.append((node.son1(), level+1))

        return max_height

    def get(self, index : int = 0):
        """
        Returns the element at the specified index in the sorted order of the binary search tree.

        Parameters:
            index (int): The index of the element to retrieve. Default is 0, which retrieves the minimum element.

        Returns:
            The element at the specified index in the sorted order of the binary search tree.

        Raises:
            IndexError: If the index is out of range.
        """
        return self[index]
    
    def exist(self, value) -> bool:
        """
        Checks if the specified value exists in the binary search tree.

        Parameters:
            value: The value to check for existence in the binary search tree.

        Returns:
            True if the value exists in the binary search tree, False otherwise.
        """
        if not isinstance(value, self.__type): raise TypeError (f"expected an '{self.__type.__name__}', but received a '{type(value).__name__}'")
        if not isinstance(value, self.__type): return False

        search  = BinaryNode(value)
        current = self.__root 

        while isinstance(current, BinaryNode):
            if search < current:
                if isinstance(current.son0(), BinaryNode): current = current.son0()
                else: return False
            elif search > current:
                if isinstance(current.son1(), BinaryNode): current = current.son1()
                else: return False
            else: return search == current
        return False

    def copy(self):
        """
        Creates a shallow copy of the binary search tree.

        Returns:
            A shallow copy of the binary search tree.
        """
        from copy import deepcopy
        return deepcopy(self)

    def levelorder(self) -> list:
        """
        Returns a list containing the elements of the binary search tree in level-order traversal order.

        Returns:
            A list containing the elements of the binary search tree in level-order traversal order.
        """
        if not isinstance(self.__root, BinaryNode): return []

        nodes = []
        queue = deque([self.__root])

        while queue:
            node = queue.popleft()
            nodes.append(node.get())

            if isinstance(node.son0(), BinaryNode): queue.append(node.son0())
            if isinstance(node.son1(), BinaryNode): queue.append(node.son1())

        return nodes

    def spiralorder(self) -> list:
        """
        Returns a list containing the elements of the binary search tree in spiral-order traversal order.

        Returns:
            A list containing the elements of the binary search tree in spiral-order traversal order.
        """
        if not isinstance(self.__root, BinaryNode): return []
        
        nodes = []

        queue = deque([self.__root])
        left_to_right = True

        while queue:
            level_size  = len(queue)
            level_nodes = []

            for _ in range(level_size):
                if left_to_right:
                    node = queue.popleft()
                    level_nodes.append(node.get())
                    if isinstance(node.son0(), BinaryNode): queue.append(node.son0())
                    if isinstance(node.son1(), BinaryNode): queue.append(node.son1())
                else: 
                    node = queue.pop()
                    level_nodes.append(node.get())
                    if isinstance(node.son1(), BinaryNode): queue.appendleft(node.son1())
                    if isinstance(node.son0(), BinaryNode): queue.appendleft(node.son0())

            nodes.extend(level_nodes)
            left_to_right = not left_to_right

        return nodes