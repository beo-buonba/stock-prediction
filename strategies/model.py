"""
DSA machine learning `Model`
"""
from abc import abstractmethod


class Model:
    """Base class for a Model

    Usage - Extend this class for all implementations of a model Implement
    all the methods declared here
    """

    name: str
    is_loaded: bool

    def __init__(self, name):
        """
        Args:
            name: str, Name of the model object
        """
        self.name = name
        self.is_loaded = False

    @abstractmethod
    def load(self):
        """
        Implement this method to load model artifacts
        :return: self
        """
        self.is_loaded = True
        return self

    @abstractmethod
    def train(self):
        """
        Implement this method to train the model
        :return: self
        """
        pass

    @abstractmethod
    def update(self):
        """
        Implement this method to update model attributes / data
        :return: self
        """
        return self

    @abstractmethod
    def predict(self, x):
        """
        Implement this method to get predictions from model
        :param x:
        :return: list of predictions
        """
        return x
