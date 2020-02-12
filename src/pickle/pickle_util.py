import pickle
import os


def save_pickle(data, file_path):
    """ Given a python object (data) and a file path (string), saves a pickle"""
    assert not os.path.exists(file_path), "file already exists, write operation canceled"
    with open(file_path, 'wb') as outfile:
        pickle.dump(data, outfile)


def load_pickle(file_path):
    """ given a file_path, loads a pickle and returns a python object"""
    with open(file_path, 'rb') as infile:
        return pickle.load(infile)
