"""
Custom (Sample) Model
"""
from services.logger import logger
from .model import Model


class SampleModel(Model):
    """
    Sample Model
    """

    def __init__(self, name):
        super().__init__(name)

    def load(self):
        """
        Dummy function - Loading model
        :return: self
        """
        logger.info(f"{self.name} loading")
        self.is_loaded = True
        return self

    def train(self):
        """
        Dummy function -  No need to implement for this example
        :return:
        """
        logger.info(f"{self.name} training")
        pass

    def update(self):
        """
        Dummy function   No need to implement for this example
        :return:
        """
        logger.info(f"{self.name} updating")
        pass

    def predict(self, x):
        """
        Dummy function to predict, simply returns the input
        :return: x
        """
        logger.info(f"{self.name} predicting")
        return x
