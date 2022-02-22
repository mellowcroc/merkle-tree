import sys
import hashlib
import math
import numpy as np
if sys.version_info < (3, 6):
    import sha3

class Node:
    def __init__(self, value, left_child=None, right_child=None):
        self.value = value
        self.left_child = left_child
        self.right_child = right_child
        self.parent = None

    def __lt__(self, other):
        return self.value < other.value

    def setParent(self, parent):
        self.parent = parent

class MerkleTree:
    def __init__(self):
        self.leafNodes = None
        self.root = None

    def create_from_data_list(self, dataList):
        self.leafNodes = self.create_leaf_nodes_from_data_list(dataList)
        self.traverse(self.leafNodes, None)

    def create_from_data(self, data, parseSize):
        self.leafNodes = self.create_leaf_nodes_from_data(data, parseSize)
        self.traverse(self.leafNodes, None)

    def create_leaf_nodes_from_data(self, data, parse_size):
        leaf_nodes = []
        data_size = len(data)
        index = 0
        while index < data_size:
            sha3 = hashlib.sha3_224()
            parseData = data[index : min(index + parse_size, data_size)]
            sha3.update(parseData)
            leaf_nodes.append(Node(sha3.hexdigest()))
            index += parse_size
        leaf_nodes.sort(reverse=True)
        return leaf_nodes

    def create_leaf_nodes_from_data_list(self, data_list):
        leaf_nodes = []
        for data in data_list:
            sha3 = hashlib.sha3_224()
            sha3.update(data.encode())
            leaf_nodes.append(Node(sha3.hexdigest()))
        leaf_nodes.sort(reverse=True)
        return leaf_nodes

    def print_pre_order(self, node):
        print("\nvalue: ", node.value)
        print("parent: ", node.parent.value if node.parent != None else node.parent)
        if node.left_child != None: self.print_pre_order(node.left_child)
        if node.right_child != None: self.print_pre_order(node.right_child)

    def print_in_order(self, node):
        if node.left_child != None: self.print_in_order(node.left_child)
        print("\nvalue: ", node.value)
        print("parent: ", node.parent.value if node.parent != None else node.parent)
        if node.right_child != None: self.print_in_order(node.right_child)

    def print_post_order(self, node):
        if node.left_child != None: self.print_post_order(node.left_child)
        if node.right_child != None: self.print_post_order(node.right_child)
        print("\nvalue: ", node.value)
        print("parent: ", node.parent.value if node.parent != None else node.parent)

    def traverse(self, nodes, oddNode):
        print("traverse")
        print("len(nodes): ", len(nodes))
        if oddNode != None:
            print("oddNode: ", oddNode.value)
        else:
            print("oddNode: ", oddNode)

        if len(nodes) == 1 and oddNode == None :
            self.root = nodes[0]
            return self.root

        if len(nodes) % 2 == 1:
            if oddNode != None:
                nodes.append(oddNode)
                oddNode = None
            else:
                oddNode = nodes.pop()

        parents = []
        for i in range(int(len(nodes) / 2)):
            left_child = nodes[i * 2]
            right_child = nodes[i * 2 + 1]
            print("left_child.value: ", left_child.value)
            print("right_child.value: ", right_child.value)
            if left_child.value < right_child.value: left_child, right_child = right_child, left_child
            print("left_child.value: ", left_child.value)
            print("right_child.value: ", right_child.value)
            
            sha3 = hashlib.sha3_224()
            sha3.update((left_child.value + right_child.value).encode())
            print("parent.value: ", sha3.hexdigest())
            parent = Node(sha3.hexdigest(), left_child, right_child)
            parents.append(parent)
            left_child.parent = parent
            right_child.parent = parent
        return self.traverse(parents, oddNode)

    def getProofs(self, leafData):
        sha3 = hashlib.sha3_224()
        sha3.update(leafData.encode())
        leafNode = self.search(self.root, sha3.hexdigest())
        if leafNode == None:
            print("could not find given leaf")
            return
        siblings = []
        self.getSibling(leafNode, siblings)
        print("siblings len: ", len(siblings))
        for i in range(len(siblings)):
            print("i: ", siblings[i])
        return siblings

    def getSibling(self, node, siblings):
        parent = node.parent
        if parent == None:
            return
        
        if node == parent.left_child:
            siblings.append(parent.right_child.value)
        else:
            siblings.append(parent.left_child.value)
        self.getSibling(parent, siblings)

    def search(self, node, value):
        if node == None:
            return None
        if node.value == value:
            return node
        
        leftResult = self.search(node.left_child, value)
        if leftResult != None: return leftResult

        rightResult = self.search(node.right_child, value)
        if rightResult != None: return rightResult

    def verify(self, root, data, siblings):
        sha3 = hashlib.sha3_224()
        sha3.update(data.encode())
        hash = sha3.hexdigest()
        for siblingHash in siblings:
            if hash < siblingHash: hash, siblingHash = siblingHash, hash
            sha3 = hashlib.sha3_224()
            sha3.update((hash + siblingHash).encode())
            hash = sha3.hexdigest()

        if root == hash: return True
        return False
