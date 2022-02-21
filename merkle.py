import sys
import hashlib
import math
import numpy as np
if sys.version_info < (3, 6):
    import sha3

SHA3 = hashlib.sha3_224()

class Node:
    value = None
    left = None
    right = None

    def __init__(self, value, left_node=None, right_node=None) -> None:
        self.value = value
        self.left = left_node
        self.right = right_node

def createLeafList(data, dataSize, leafMaxSize):
    leaf_list = []
    while dataSize > 0:
        SHA3.update(data)

        dataSize -= leafMaxSize
        leaf_list.append(SHA3.hexdigest())
    return leaf_list

def getNodeCountAtNextDepth(currDepth):
    return math.ceil(currDepth / 2)

def printMerkleTree(node):
    if node.left != None: printMerkleTree(node.left)
    if node.right != None: printMerkleTree(node.right)

# given current index, check if the index * 2 and index * 2 + 1 values exist
# if index * 2 exist, create left node,
# if index * 2 + 1 exist, create right node

# traverse(root, 0, 0)
def traverse(nodes, root, depth, index):
    if depth == len(nodes) - 1: return

    if index * 2 == len(nodes[depth + 1]) - 1:
        # left only
        root.left = Node(nodes[depth + 1][index * 2], None, None)
        traverse(nodes, root.left, depth + 1, index * 2)
    else:
        # left and right
        root.left = Node(nodes[depth + 1][index * 2], None, None)
        root.right = Node(nodes[depth + 1][index * 2 + 1], None, None)
        traverse(nodes, root.left, depth + 1, index * 2)
        traverse(nodes, root.right, depth + 1, index * 2 + 1)

def createMerkleHashArrays(leafList, treeHeight):
    nodes = []
    nodes.append(leafList)

    prevDepthNodeCount = len(leafList) # 5
    currDepthNodeCount = getNodeCountAtNextDepth(prevDepthNodeCount) # 3

    prevDepthNodes = leafList
    currDepthNodes = []

    for depth in range(1, treeHeight): # 1, 2, 3
        index = 0

        while index < prevDepthNodeCount:
            if index + 1 == prevDepthNodeCount:
                currDepthNodes.append(prevDepthNodes[index])
            else:
                SHA3.update((prevDepthNodes[index] + prevDepthNodes[index + 1]).encode())
                currDepthNodes.append(SHA3.hexdigest())
            index += 2
        nodes.insert(0, currDepthNodes)
        prevDepthNodes = currDepthNodes
        currDepthNodes = []
        prevDepthNodeCount = currDepthNodeCount
        currDepthNodeCount = getNodeCountAtNextDepth(currDepthNodeCount)
    return nodes

def create(data, leafMaxSize):
    dataSize = len(data)
    if dataSize == 0:
        sys.exit("size should be greater than 0")

    leafList = createLeafList(data, dataSize, leafMaxSize)

    treeHeight = math.ceil(math.log2(len(leafList))) + 1

    nodes = createMerkleHashArrays(leafList, treeHeight)

    root = Node(nodes[0][0], None, None)
    traverse(nodes, root, 0, 0)
    return root


def verify(root, data, siblings):
    SHA3.update(data)
    hash = SHA3.hexdigest()
    print("first hash: ", hash)
    for sibling in siblings:
        hash = SHA3.update((hash + sibling).encode())
        print("new hash: ", hash)

    if root == hash: return True
    return False
