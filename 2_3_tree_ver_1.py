class Node:
    last_referred = list()

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
                return True, self
            elif user_input < left:
                Node.last_referred.append("left")
                return self.childs["left"].search(user_input)
            elif user_input > right:
                Node.last_referred.append("right")
                return self.childs["right"].search(user_input)
            else:
                Node.last_referred.append("mid")
                return self.childs["mid"].search(user_input)
        else:
            if user_input in self.data:
                return True, self
            else:
                return False, None

    def delete(self, user_input):
        Node.last_referred.clear()
        is_it_exist, delete_node = self.search(user_input)
        if is_it_exist:
            if delete_node.childs:
                if user_input == max(delete_node.data):
                    right_subtree = delete_node.child["right"]
                    Node.last_referred.append("right")
                    delete_data_index = 1
                else:
                    right_subtree = delete_node.child["mid"]
                    Node.last_referred.append("mid")
                    delete_data_index = 0

                successor_node = right_subtree.find_successor()
                successor = successor_node.pop(0)
                delete_node.data.pop(delete_data_index)
                delete_node.data.append(successor)
                delete_node.data.sort()

                if not successor_node.data:
                    successor_node.underflow()
            else:
                if user_input == max(delete_node.data):
                    delete_node.data.pop()
                else:
                    delete_node.data.pop(0)
                delete_node.data.sort()
                if not delete_node.data:
                    delete_node.underflow()

        else:
            print("Data does not exist")

    def underflow(self):
        if self.parent is not None:
            index = Node.last_referred.pop()
            if self.childs:
                if index == "left":
                    if len(self.parent.data) == 2:
                        if len(self.parent.childs["mid"].data) == 2:
                            add_data = self.parent.childs["mid"].data.pop(0)
                            left_child_data = self.parent.data.pop(0)
                            self.parent.data.append(add_data)
                            self.parent.data.sort()
                            self.data.append(left_child_data)
                            self.childs["right"] = self.parent.childs["mid"].childs["left"]
                            self.childs["left"] = self.childs["underflow"]
                            self.parent.childs["mid"].childs["left"] = self.parent.childs["mid"].childs["mid"]
                            del self.parent.childs["mid"].childs["mid"]
                            del self.childs["underflow"]
                        else:
                            add_data = self.parent.childs["mid"].data.pop(0)
                            left_child_data = self.parent.data.pop(0)
                            self.data.append(left_child_data)
                            self.data.append(add_data)
                            self.data.sort()
                            self.childs["left"] = self.childs["underflow"]
                            self.childs["mid"] = self.parent.childs["mid"].childs["left"]
                            self.childs["right"] = self.parent.childs["mid"].childs["right"]
                            del self.parent.childs["mid"].childs["left"]
                            del self.parent.childs["mid"].childs["right"]
                            del self.parent.childs["mid"]

                    elif len(self.parent.data) == 1:
                        if len(self.parent.childs["right"].data) == 2:
                            add_data = self.parent.childs["right"].data.pop(0)
                            left_child_data = self.parent.data.pop(0)
                            self.parent.data.append(add_data)
                            self.parent.data.sort()
                            self.data.append(left_child_data)
                            self.childs["left"] = self.childs["underflow"]
                            self.childs["right"] = self.parent.childs["right"].childs["left"]
                            self.parent.childs["right"].childs["left"] = self.parent.childs["right"].childs["mid"]
                            del self.childs["underflow"]
                            del self.parent.childs["right"].childs["mid"]
                        else:
                            left_child_data = self.parent.data.pop(0)
                            add_data = self.parent.childs["right"].data.pop(0)
                            self.data.append(left_child_data)
                            self.data.append(add_data)
                            self.data.sort()
                            self.childs["left"] = self.childs["underflow"]
                            self.childs["mid"] = self.parent.childs["right"].childs["left"]
                            self.childs["right"] = self.parent.childs["right"].childs["right"]
                            self.parent.childs["underflow"] = self.parent.childs["left"]
                            del self.parent.childs["left"]
                            del self.parent.childs["right"].childs["left"]
                            del self.parent.childs["right"].childs["right"]
                            del self.parent.childs["right"]
                            self.parent.underflow()

                elif index == "mid":
                    if len(self.parent.childs["left"].data) == 2:
                        add_data = self.parent.childs["left"].data.pop(1)
                        mid_child_data = self.parent.data.pop(0)
                        self.parent.data.append(add_data)
                        self.parent.data.sort()
                        self.data.append(mid_child_data)
                        self.childs["left"] = self.parent.childs["left"].childs["right"]
                        self.childs["right"] = self.childs["underflow"]
                        self.parent.childs["left"].childs["right"] = self.parent.childs["left"].childs["mid"]
                        del self.childs["underflow"]
                        del self.parent.childs["left"].childs["mid"]

                    elif len(self.parent.childs["right"].data) == 2:
                        add_data = self.parent.childs["right"].data.pop(0)
                        mid_child_data = self.parent.data.pop(1)
                        self.parent.data.append(add_data)
                        self.parent.data.sort()
                        self.data.append(mid_child_data)
                        self.childs["right"] = self.parent.childs["right"].childs["left"]
                        self.childs["left"] = self.childs["underflow"]
                        self.parent.childs["right"].childs["left"] = self.parent.childs["right"].childs["mid"]
                        del self.childs["underflow"]
                        del self.parent.childs["right"].childs["mid"]

                    else:
                        add_data = self.parent.childs["left"].data.pop(0)
                        mid_child_data = self.parent.data.pop(0)
                        self.data.append(add_data)
                        self.data.append(mid_child_data)
                        self.data.sort()
                        self.childs["left"] = self.parent.childs["left"].childs["left"]
                        self.childs["mid"] = self.parent.childs["left"].childs["right"]
                        self.childs["right"] = self.childs["underflow"]
                        self.parent.childs["left"] = self.parent.childs["mid"]
                        del self.childs["underflow"]
                        del self.parent.childs["mid"]

                elif index == "right":
                    if len(self.parent.data) == 2:
                        if len(self.parent.childs["mid"].data) == 2:
                            add_data = self.parent.childs["mid"].data.pop(1)
                            right_child_data = self.parent.data.pop(1)
                            self.parent.data.append(add_data)
                            self.parent.data.sort()
                            self.data.append(right_child_data)
                            self.childs["right"] = self.childs["underflow"]
                            self.childs["left"] = self.parent.childs["mid"].childs["right"]
                            self.parent.childs["mid"].childs["right"] = self.parent.childs["mid"].childs["mid"]
                            del self.parent.childs["mid"].childs["mid"]
                            del self.childs["underflow"]
                        else:
                            add_data = self.parent.childs["mid"].data.pop(0)
                            right_child_data = self.parent.data.pop(1)
                            self.data.append(right_child_data)
                            self.data.append(add_data)
                            self.data.sort()

                            self.childs["right"] = self.childs["underflow"]
                            self.childs["mid"] = self.parent.childs["mid"].childs["right"]
                            self.childs["left"] = self.parent.childs["mid"].childs["left"]
                            del self.parent.childs["mid"].childs["left"]
                            del self.parent.childs["mid"].childs["right"]
                            del self.parent.childs["mid"]

                    elif len(self.parent.data) == 1:
                        if len(self.parent.childs["left"].data) == 2:
                            add_data = self.parent.childs["left"].data.pop(1)
                            right_child_data = self.parent.data.pop(0)
                            self.parent.data.append(add_data)
                            self.parent.data.sort()
                            self.data.append(right_child_data)
                            self.childs["right"] = self.childs["underflow"]
                            self.childs["left"] = self.parent.childs["left"].childs["right"]
                            self.parent.childs["left"].childs["right"] = self.parent.childs["left"].childs["mid"]
                            del self.childs["underflow"]
                            del self.parent.childs["left"].childs["mid"]
                        else:
                            right_child_data = self.parent.data.pop(0)
                            add_data = self.parent.childs["left"].data.pop(0)
                            self.data.append(right_child_data)
                            self.data.append(add_data)
                            self.data.sort()
                            self.parent.childs["underflow"] = self.parent.childs["right"]
                            self.childs["left"] = self.parent.childs["left"].childs["left"]
                            self.childs["mid"] = self.parent.childs["left"].childs["right"]
                            self.childs["right"] = self.childs["underflow"]
                            self.parent.childs["underflow"] = self.parent.childs["right"]
                            del self.parent.childs["right"]
                            del self.parent.childs["left"].childs["left"]
                            del self.parent.childs["left"].childs["right"]
                            del self.parent.childs["left"]
                            self.parent.underflow()

            elif not self.childs:
                if index == "left":
                    if len(self.parent.data) == 2:
                        if len(self.parent.childs["mid"].data) == 2:
                            add_data = self.parent.childs["mid"].data.pop(0)
                            left_child_data = self.parent.data.pop(0)
                            self.parent.data.append(add_data)
                            self.parent.data.sort()
                            self.data.append(left_child_data)
                        else:
                            add_data = self.parent.childs["mid"].data.pop(0)
                            left_child_data = self.parent.data.pop(0)
                            self.data.append(left_child_data)
                            self.data.append(add_data)
                            self.data.sort()
                            del self.parent.childs["mid"]

                    elif len(self.parent.data) == 1:
                        if len(self.parent.childs["right"].data) == 2:
                            add_data = self.parent.childs["right"].data.pop(0)
                            left_child_data = self.parent.data.pop(0)
                            self.parent.data.append(add_data)
                            self.parent.data.sort()
                            self.data.append(left_child_data)
                        else:
                            left_child_data = self.parent.data.pop(0)
                            add_data = self.parent.childs["right"].data.pop(0)
                            self.data.append(left_child_data)
                            self.data.append(add_data)
                            self.data.sort()
                            self.parent.childs["underflow"] = self.parent.childs["left"]
                            del self.parent.childs["left"]
                            del self.parent.childs["right"]
                            self.parent.underflow()

                elif index == "mid":
                    if len(self.parent.childs["left"].data) == 2:
                        add_data = self.parent.childs["left"].data.pop(1)
                        mid_child_data = self.parent.data.pop(0)
                        self.parent.data.append(add_data)
                        self.parent.data.sort()
                        self.data.append(mid_child_data)
                    elif len(self.parent.childs["right"].data) == 2:
                        add_data = self.parent.childs["right"].data.pop(0)
                        mid_child_data = self.parent.data.pop(1)
                        self.parent.data.append(add_data)
                        self.parent.data.sort()
                        self.data.append(mid_child_data)
                    else:
                        add_data = self.parent.childs["left"].data.pop(0)
                        mid_child_data = self.parent.data.pop(0)
                        self.data.append(add_data)
                        self.data.append(mid_child_data)
                        self.data.sort()
                        self.parent.childs["left"] = self.parent.childs["mid"]
                        del self.parent.childs["mid"]

                elif index == "right":
                    if len(self.parent.data) == 2:
                        if len(self.parent.childs["mid"].data) == 2:
                            add_data = self.parent.childs["mid"].data.pop(1)
                            right_child_data = self.parent.data.pop(1)
                            self.parent.data.append(add_data)
                            self.parent.data.sort()
                            self.data.append(right_child_data)
                        else:
                            add_data = self.parent.childs["mid"].data.pop(0)
                            right_child_data = self.parent.data.pop(1)
                            self.data.append(right_child_data)
                            self.data.append(add_data)
                            self.data.sort()
                            del self.parent.childs["mid"]

                    elif len(self.parent.data) == 1:
                        if len(self.parent.childs["left"].data) == 2:
                            add_data = self.parent.childs["left"].data.pop(1)
                            right_child_data = self.parent.data.pop(0)
                            self.parent.data.append(add_data)
                            self.parent.data.sort()
                            self.data.append(right_child_data)
                        else:
                            right_child_data = self.parent.data.pop(0)
                            add_data = self.parent.childs["left"].data.pop(0)
                            self.data.append(right_child_data)
                            self.data.append(add_data)
                            self.data.sort()
                            self.parent.childs["underflow"] = self.parent.childs["right"]
                            del self.parent.childs["left"]
                            del self.parent.childs["right"]
                            self.parent.underflow()

    def find_successor(self):
        if self.childs:
            Node.last_referred.append("left")
            self.childs["left"].find_successor()
        else:
            return self

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


def change_top(top_of_node):
    if "underflow" in top_of_node.childs:
        return top_of_node.childs["underflow"]


tree = Node(1)
tree.insert(4)
tree.insert(5)
tree.insert(8)
tree.insert(-1)
tree.insert(9)
tree.insert(10)
tree.insert(6)
tree.insert(6)
tree.insert(11)

tree.delete(-1)
tree.delete(1)
tree.delete(5)
tree.delete(4)
tree = change_top(tree)
print(tree.data)
print(tree.childs["left"].data)
print(tree.childs["mid"].data)
print(tree.childs["right"].data)
