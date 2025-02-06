################################################################################
# 
#     Author:      Lorenzo D. Moon
#     Instructor:  Karla Fant
#     Course:      CS-302
#     Assignment:  Program 4/5
#     Description: Test Suite for TextToDict and TextToList 
#
################################################################################

import pytest
from text_loader import TextToDict, TextToList

def test_text_to_dict():
    '''
    Test the TextToDict class
    There's only a couple of methods to test so it's all in one test 
    '''
    text_to_dict = TextToDict()
    assert text_to_dict.data == []
    text_to_dict.load_file("test_data/test_dict.txt")
    
    assert text_to_dict.data == [
        {"key1": "string", "key2": 123, "key3": True},
        {"key1": "string2", "key2": 456, "key3": False}]
    
    with pytest.raises(FileNotFoundError):
        text_to_dict.load_file("garbage")

def test_text_to_list():
    '''
    Test the TextToList class
    There's only a couple of methods to test so it's all in one test
    '''
    text_to_list = TextToList()
    assert text_to_list.data == []

    text_to_list.load_file("./test_data/test_list.txt")

    assert text_to_list.data == [
            "one", "two", "three", "four", "five", "six", "seven"]
    
    with pytest.raises(FileNotFoundError):
        text_to_list.load_file("FakeFile.txt")

if __name__ == "__main__":
    pytest.main(["-v", "test_text_loader.py"])