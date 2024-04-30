import numpy as np
import torch
from sklearn.base import BaseEstimator, ClassifierMixin
from torch import nn


class PyTorchWrapper(BaseEstimator, ClassifierMixin):
    def __init__(self, model_config, **kwargs):

        self.model = self.build_model(model_config)

    def build_model(self, model_configs):
        pass

    def fit(self):
        pass

    def predict(self):
        pass

    def predict_proba(self):
        pass
