################################################################################
# 
#     Author:      Lorenzo D. Moon
#     Instructor:  Karla Fant
#     Course:      CS-302
#     Assignment:  Program 4/5
#     Description: 2-3 Tree and Node class Test Suite
#
################################################################################

import pytest
from tree import Node, Tree
from encounter_generator import EncounterGenerator

def test_node_init():
    node = Node()
    assert node.data == []
    assert node.children == []

def test_node_split_leaf():
    node = Node()
    assert str(node) == "()"
    node.insert(10)
    assert str(node) == "(10)"
    assert node.is_full() == False
    assert node.split() == None
    node.insert(20)
    assert str(node) == "(10, 20)"
    assert node.is_full() == False
    assert node.split() == None
    node.insert(15)
    assert node.is_full() == True
    split_node = node.split()
    assert str(split_node) == "(15)"
    assert str(split_node.children) == "[(10), (20)]"

def test_tree_init():
    tree = Tree()
    assert tree.root == None
    data_input = [10, 20, 15, 9, 8, 12, 11]
    for data in data_input:
        tree.insert(data)
    
    assert str(tree.root) == "(11)"
    assert str(tree.root.children) == "[(9), (15)]"
    assert str(tree.root.children[0].children) == "[(8), (10)]"
    assert str(tree.root.children[1].children) == "[(12), (20)]"
    assert "LETS GOOOOO" == "LETS GOOOOO"

def test_display_tree():
    tree = Tree()
    data_input = [10, 20, 15, 9, 8, 12, 11]
    for data in data_input:
        tree.insert(data)
    assert str(tree) == "8 9 10 11 12 15 20"

def test_retrive(tree_fixture, tree_data):
    tree = tree_fixture
    data = tree_data

    for d in data:
        assert tree.retrieve(d) == d

    this = True
    miracle = True
    assert this == miracle

def test_with_encounter_generator(tree_fixture):
    # I had a huge problem with the tree crashing. It worked with numbers.
    # But it didn't work with entities. I used this test to fix the entity
    # class and the tree class. It works now!
    
    # It generates 1000 encounters and inserts them into the tree
    eg = EncounterGenerator()
    tree = Tree()

    for i in range(1000):
        encounter = eg.encounter(0, 100)
        if encounter is not None:
            tree.insert(encounter)

if __name__ == "__main__":
    pytest.main(["-v", "test_tree.py"])