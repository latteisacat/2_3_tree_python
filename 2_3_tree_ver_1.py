class Node:
    last_referred = list()
    top_of_node = None

    def __init__(self, data, parent=None):
        self.childs = dict()
        self.data = list()
        self.data.append(data)
        self.parent = parent

    def insert(self, user_input):
        Node.last_referred.clear()
        input_node = self.input_search(user_input)
        input_node.add(user_input)

    def input_search(self, user_input):
        if self.childs:
            left = min(self.data)
            right = max(self.data)
            if user_input <= left:
                Node.last_referred.append("left")
                return self.childs["left"].input_search(user_input)
            elif user_input > right:
                Node.last_referred.append("right")
                return self.childs["right"].input_search(user_input)
            else:
                Node.last_referred.append("mid")
                return self.childs["mid"].input_search(user_input)
        else:
            return self

    def split(self):
        if self.parent is None and self.childs:
            index = Node.last_referred.pop()
            new_left_node = Node(self.data.pop(0), self)
            new_right_node = Node(self.data.pop(1), self)
            if index == "left":
                new_left_node.childs["left"] = self.childs["left"]
                new_left_node.childs["right"] = self.childs["overflow"]
                new_right_node.childs["left"] = self.childs["mid"]
                new_right_node.childs["right"] = self.childs["right"]
            elif index == "right":
                new_left_node.childs["left"] = self.childs["left"]
                new_left_node.childs["right"] = self.childs["mid"]
                new_right_node.childs["left"] = self.childs["right"]
                new_right_node.childs["right"] = self.childs["overflow"]
            elif index == "mid":
                new_left_node.childs["left"] = self.childs["left"]
                new_left_node.childs["right"] = self.childs["mid"]
                new_right_node.childs["left"] = self.childs["overflow"]
                new_right_node.childs["right"] = self.childs["right"]

            new_left_node.childs["left"].parent = new_left_node
            new_left_node.childs["right"].parent = new_left_node
            new_right_node.childs["left"].parent = new_right_node
            new_right_node.childs["right"].parent = new_right_node
            self.childs["left"] = new_left_node
            self.childs["right"] = new_right_node
            del self.childs["mid"]
            del self.childs["overflow"]

        elif self.parent is not None and self.childs:
            index = Node.last_referred.pop()
            new_node = Node(self.data.pop(), self.parent)
            self.parent.childs["overflow"] = new_node
            if index == "left":
                new_node.childs["left"] = self.childs["mid"]
                new_node.childs["right"] = self.childs["right"]
                self.childs["right"] = self.childs["overflow"]

            elif index == "right":
                new_node.childs["left"] = self.childs["right"]
                new_node.childs["right"] = self.childs["overflow"]
                self.childs["right"] = self.childs["mid"]

            elif index == "mid":
                new_node.childs["left"] = self.childs["overflow"]
                new_node.childs["right"] = self.childs["right"]
                self.childs["right"] = self.childs["mid"]

            new_node.childs["left"].parent = new_node
            new_node.childs["right"].parent = new_node

            del self.childs["mid"]
            del self.childs["overflow"]

        elif self.parent is None and not self.childs:
            self.childs["left"] = Node(self.data.pop(0), self)
            self.childs["right"] = Node(self.data.pop(1), self)
        elif self.parent is not None and not self.childs:
            self.parent.childs["overflow"] = Node(self.data.pop(), self.parent)

    def search(self, user_input):
        if self.childs:
            left = min(self.data)
            right = max(self.data)
            if user_input in self.data:
                return True
            elif user_input < left:
                return self.childs["left"].search(user_input)
            elif user_input > right:
                return self.childs["right"].search(user_input)
            else:
                return self.childs["mid"].search(user_input)
        else:
            if self.data in user_input:
                return True
            else:
                return False

    def delete(self, user_input):
        pass

    def underflow(self, data):
        pass

    def add(self, user_input):
        self.data.append(user_input)
        self.data.sort()

        if len(self.data) == 3:
            self.split()
            if self.parent is not None:
                self.parent.add(self.data.pop())
        elif "overflow" in self.childs:
            index = Node.last_referred.pop()
            if index == "left":
                self.childs["mid"] = self.childs["overflow"]
            elif index == "right":
                self.childs["mid"] = self.childs["right"]
                self.childs["right"] = self.childs["overflow"]
            del self.childs["overflow"]


tree = Node(1)
tree.insert(4)
tree.insert(5)
tree.insert(8)
tree.insert(-1)
tree.insert(9)
tree.insert(10)
tree.insert(6)
tree.insert(6)
print(tree.data)
print(tree.childs["left"].data)
print(tree.childs["right"].data)
print(tree.childs["left"].childs["left"].data)
print(tree.childs["left"].childs["right"].data)
print(tree.childs["right"].childs["left"].data)
print(tree.childs["right"].childs["right"].data)