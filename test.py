from merkle import MerkleTree

def test_data_list():
    dataList = ["a", "b", "c", "d", "e"]
    merkle = MerkleTree()
    merkle.create_from_data_list(dataList)
    expectedRootValue = b'550772be11d74b2f729c534b0b2dba7958feb0ad7667d7f7f1cc5bf8'
    assert merkle.root.value.encode() == expectedRootValue

    siblings = merkle.getProofs("a")
    assert merkle.verify(merkle.root.value, "a", siblings) == True

if __name__ == "__main__":
    test_data_list()