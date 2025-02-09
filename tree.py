################################################################################
# 
#     Author:      Lorenzo D. Moon
#     Instructor:  Karla Fant
#     Course:      CS-302
#     Assignment:  Program 4/5
#     Description: 2-3 Tree and Node class.
#
################################################################################

class Node:
    def __init__(self) -> None:
        self.__data = []       # Holds 1, 2, or 3 values (3 for a ready to split node)
        self.__children = []   # Holds 0, 2, or 3 children (Never 1 child!)

    def __del__(self) -> None:
        # Zero out the data and children lists.
        self.__data = []
        self.__children = []

    def __str__(self) -> str:
        '''
        This is the string representation of the node.
        () FOR EMPTY NODE
        ( DATA1 ) OR ( DATA1, DATA2 ) 
        ( DATA1, DATA2, DATA3) FOR A READY TO SPLIT NODE 
        (This should never be seen by the user, but it's here for debugging.)
        Lists will be represented as [SUB_DATA_A, SUB_DATA_B, ETC]
        '''
        output = f"("
        for i in range(len(self.__data)):
            output += f"{self.__data[i]}"
            if i < len(self.__data) - 1:
                output += ", "
        output += ")"
        return output 
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> bool:
        # FOR TESTING NODE == NODE.
        # NODE SHOULD NEVER BE INSTANTIATED OUTSIDE 2-3 TREE
        # This is needed when comparing to None apparently. Why, god? 
        if other == None: return False

        if isinstance(other, Node):
            return self.data == other.data
        
        return self.data == other
    
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Node):
            raise TypeError("Can only compare a Node to another Node.")

        if self.data == [] or other.data == []:
            raise ValueError("Cannot compare an empty Node to a non-empty Node.")
        
        if type(self.data[0]) == list:
            return self.data[0][0] < other.data[0]
        
        if type(other.data[0]) == list:
            return self.data[0] < other.data[0][0]
        
        return self.data[0] < other.data[0]
        
    def __iadd__(self, other: object) -> None:
        # This makes it so the split can happen and return a node.
        # Then the tree class combines the split with it's parent.
        # This took me so long to figure out. I have been working on it since
        # program 3.
        if not isinstance(other, Node):
            raise TypeError("Can only add a Node to another Node.")
        
        # There will be an empty child when the node is split.
        # It removes the data from the split node and leaves a husk.
        # This removes it from the parent.
        self.__remove_husks() 

        # Adopt the children from the rhs node
        for children in other.children:
            self.__adopt(children)
        
        # Gain the data from the rhs node
        for data in other.data:
            self.insert(data)
        
        return self
    
    @property
    def data(self) -> list:
        return self.__data
    
    @property
    def children(self) -> list:
        return self.__children
    
    def is_leaf(self) -> bool:
        return self.__children == []
    
    def is_full(self) -> bool:
        return len(self.__data) == 3

    def add_dup(self, new_data) -> bool:
        # If there is duplicate data, add it to the list.
        # If there is no list, make it a list
        for i in range(len(self.__data)): 
            if type(self.__data[i]) == list:          # If the data is a list...
                if self.__data[i][0] == new_data:     # and it matches the first element...
                    self.data[i].append(new_data)     # append the new data to the list.
                    return True
            else:
                if self.__data[i] == new_data:        # If the data is not a list...
                    self.__data[i] = [self.__data[i]] # turn it into a list...
                    self.__data[i].append(new_data)   # and append the new data.
                    return True
        return False
    
    def insert(self, new_data) -> None:
        # If it's duplicate data, add it to the list.
        if self.add_dup(new_data): return

        # If it's new data, add it to the list and sort the list.
        self.__data.append(new_data)
        self.__data.sort(key=self.__sort_key())
        return
    
    def split(self):
        # If we're not full, we can't split.
        if not self.is_full(): return None

        split_node = Node()                   # Make a new node
        split_node.insert(self.__data.pop(1)) # Move the middle value into the new node

        left = Node()                         # Make a new left node
        left.insert(self.__data.pop(0))       # Move the left data into that node

        right = Node()                        # Make a new right node
        right.insert(self.__data.pop(0))      # Move the right data into that node
    
        split_node.__adopt(left)              # Adopt the left and right nodes
        split_node.__adopt(right)             # Into the new node

        # If the node is not a leaf, adopt the children
        if not self.is_leaf():
            left.__adopt(self.__children.pop(0))  # Move the first two children
            left.__adopt(self.__children.pop(0))  # to the left node
            right.__adopt(self.__children.pop(0)) # Move the remaining children
            right.__adopt(self.__children.pop(0)) # to the right node
        
        # THIS NODE IS NOW A HUSK. IT HAS NO DATA. IT'S A GHOST OF THE SPLIT NODE.
        # Return the new split node
        return split_node


   
    def __sort_key(self):
        '''
        This is a helper function for the sort method.
        It returns a lambda function that gets a key for "sort"
        If the data is a list, it returns the first element.
        This is used to sort the data in the node.
        Vital for when __data has lists of a type AND a type 
        I tried using "__sort_key" as a method with params and it threw an error
        every time. I feel like this is not the right way to use a lamba, but it
        works.
        '''
        return lambda key: key[0] if type(key) == list else key
    
    def __adopt(self, new_child) -> None:
        # If the new child is None, don't adopt it.
        if new_child == None: return

        # Adopt the new child and sort the children.
        self.__children.append(new_child)
        self.__children.sort(key=self.__sort_key())
    
    def compare(self, data):
        # Compare the data to the data in the node.
        for i in range(len(self.__data)):
            if type(self.__data[i]) == list:
                if data < self.__data[i][0]:
                    return i
            elif data < self.__data[i]:
                return i
            
        return len(self.__data)
    
    def __remove_husks(self):
        # There will be a husk child every split in the parent node.
        # A ghost of the split node that has all it's data removed
        for child in self.__children:
            if child.data == []:
                self.__children.remove(child)
        return
    
class Tree:
    ''' 2-3 Tree '''
    def __init__(self):
        self.__root = None 
    
    def __del__(self):
        self.__root = None

    def insert(self, data):
        # If the tree is empty, make a new root and insert the data.
        if self.__root == None:
            self.__root = Node()
            self.__root.insert(data)
            return
        
        # If the tree is not empty, insert the data into the tree.
        new_root = self.__insert(self.__root, data)

        # If there's not a new root, we're done
        if new_root == None: return

        # If there is a new root, make it the new root.
        self.__root = new_root
        return 
    
    def __insert(self, root, data):
        '''
        Inserts the data into the tree and handles requesting a split.
        If there is a split it will rejoin as it unwinds the stack.
        If the root is split, it will return the new root.
        '''

        # If the data exists in the current node, we're done. Add it and leave
        if root.add_dup(data): return None

        # If the node is a leaf, add the data, check for a split, 
        # and return a split if there is one.
        if root.is_leaf():
            root.insert(data)
            return root.split()

        # If the node is not a leaf, find the index to head towards
        index = root.compare(data)
        split = self.__insert(root.children[index], data)

        # If there wasn't a split, we're done.
        if split == None: return None

        # If there was a split, join the split node to the current node.
        root += split

        # If that resulted in ANOTHER split, keep splitting as the stack
        # unwinds
        return root.split()
    
    def __str__(self):
        return(self.string_in_order())
    
    def display(self) -> None:
        print(self.string_in_order())
    
    def list_in_order(self) -> list:
        # If the tree is empty, return an empty list
        if self.__root == None: return []

        # If the tree is not empty, return the in order traversal of the tree.
        return self.__in_order(self.__root, '\n').split('\n')
    
    def string_in_order(self, delimiter=" ") -> str:
        # If the tree is empty, return "Empty Tree"
        if self.__root == None: return "Empty Tree"

        # If the tree is not empty, return the in order traversal of the tree.
        output = self.__in_order(self.__root, delimiter)

        return output.strip() # Remove the trailing space
    
    def __in_order(self, root, delimiter=" ") -> str:
        # If the node is empty, return an empty string
        if root == None: return ""

        output = "" # Start with an empty string

        # If the node has children, traverse the left child
        if len(root.children) > 0:
            output += self.__in_order(root.children[0], delimiter)
        
        # Add the data to the output string
        if isinstance(root.data[0], list):
            for data in root.data[0]:
                output += str(data) + delimiter
        else:
            output += str(root.data[0]) + delimiter 

        # If there is a second child, traverse it
        if len(root.children) > 1:
            output += self.__in_order(root.children[1], delimiter)
        
        # If there is a second data, add it to the output string

        if len(root.data) == 2:
            if isinstance(root.data[1], list):
                for data in root.data[1]:
                    output += str(data) + delimiter
            else:
                output += str(root.data[1]) + delimiter 
        
        # If there is a third child, traverse it
        if len(root.children) > 2:
            output += self.__in_order(root.children[2], delimiter)

        # Return the output string
        return output
    
    def __repr__(self):
        return self.__str__()
    
    def retrieve(self, data):
        # If the tree is empty, return None
        if self.__root == None: return None

        # If the tree is not empty, retrieve the data.
        return self.__retrieve(self.__root, data)
    
    def __retrieve(self, root, key):
        # If the data is in the current node, return it.
        for data in root.data:
            if key == data: return data 
            if type(data) == list and key == data[0]: return data 

        # If the data is not in the current node, and it's a leaf, return None
        if root.is_leaf(): return None

        # If the data is not in the current node, and it's not a leaf,
        # find the index to head towards and keep searching.
        index = root.compare(key)
        return self.__retrieve(root.children[index], key)

    @property
    def root(self):
        return self.__root