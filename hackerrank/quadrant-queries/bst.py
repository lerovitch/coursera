class Node(object):

    def __init__(self, value=None, parent=None):
        self.value = value
        self.parent = parent
        self.left = None
        self.right = None
        self.size = 1 if value else 0

    def insert(self, node):
        if self.value is None:
            if not isinstance(node, Node):
                self.value = node
            else:
                self.value = node.value
            return 

        if not isinstance(node, Node):
            node = Node(node)

        self.size += 1
        if self.value >= node.value:
            if self.left:
                self.left.insert(node)
            else:
                self.left = node
                node.parent = self
        elif self.value < node.value:
            if self.right:
                self.right.insert(node)
            else:
                self.right = node
                node.parent = self

    def get(self, value):
        if self.value == value:
            return self
        elif self.value >= value:
            if self.left:
                return self.left.get(value)
        elif self.right:
            return self.right.get(value)
        return None

    def delete_min(self):
        if self.parent:
            if self.parent.right == self:
                self.parent.right = None
            else:
                self.parent.left = None
        else:
            self.value = None
            self.right = None
            self.left = None

    def delete_wone_children(self):
        if self.parent:
            if self.right:
                if self.parent.right == self:
                    self.parent.right = self.right
                    self.right.parent = self.parent
                else:
                    self.parent.left = self.right
                    self.right.parent = self.parent
            else:
                if self.parent.right == self:
                    self.parent.right = self.left
                    self.left.parent = self.parent
                else:
                    self.parent.left = self.left
                    self.left.parent = self.parent
        else:
            self.value = (self.right and self.right.value) or (self.left and self.left.value)
            self.right = None
            self.left = None


    def min(self):
        if self.left:
            return self.left.min()
        else:
            return self

    def interval(self, i_min, i_max, ls=None): 
        if ls is None:
            ls = []
        if self.left and self.left.value >= i_min:
            self.left.interval(i_min, i_max, ls)
        if i_max >= self.value and i_min <= self.value:
            ls.append(self.value)
        if self.right and self.right.value <= i_max:
            self.right.interval(i_min, i_max, ls)
        return ls

    def inorder(self, ls=None): 
        if ls is None:
            ls = []
        if self.left:
            self.left.inorder(ls)
        ls.append(self)
        if self.right:
            self.right.inorder(ls)
        return ls

    def delete(self, value):
        deleted = 0
        if self.right and self.value < value:
            deleted = self.right.delete(value)

        elif self.left and self.value > value:
            deleted = self.left.delete(value)
        elif self.value == value:
            if not self.left and not self.right:
                self.delete_min()
                deleted = 1
            elif (not self.left and self.right) or (not self.right and self.left):
                self.delete_wone_children()
                deleted = 1
            else:
                successor = self.right.min()
                if successor.value == self.value:
                    import ipdb; ipdb.set_trace()
                self.delete(successor.value)
                self.value = successor.value
        self.size -= deleted
        return deleted

    def __repr__(self):
        left = str(self.left.value) if self.left else ""
        right = str(self.right.value) if self.right else ""
        return "(" + str(self.value) + ")" + " size: " + str(self.size) + " left:" + left + " right:" + right

    def __str__(self):
            return self.__repr__()
