"""Downloads datasets and splits in train/test."""

import pickle
import tempfile

class Dataset:
    """Managing dataset in the high level interface."""

    def __init__(self):
        self.file = tempfile.TemporaryFile()

    def update(self,data):
        """Update the content of the dataset."""
        pickle.dump(data,self.file)
        self.file.seek(0)

    def __str__(self):
        return str(self.load())

    def load(self):
        """Return the dataset loaded into memory.

        :return: Previously updated dataset.
        :rtype: pandas.dataframe for adul or dictionary of numpy.ndarray for utkfaces"""
        data = pickle.load(self.file)
        self.file.seek(0)
        return data
