from typing import Any, Dict, List, Optional

import mlflow
import numpy as np
import torch.nn as nn
from sklearn.base import BaseEstimator

from evaluation.metrics import Metrics


class Experiment:
    def __init__(self, train_data: np.ndarray, train_labels: np.ndarray, test_data: np.ndarray, test_labels: np.ndarray,
                 dataset_chars: dict, label_names: List[str]):
        self.train_data = train_data
        self.train_labels = train_labels
        self.test_data = test_data
        self.test_labels = test_labels
        self.dataset_chars = dataset_chars
        self.label_names = label_names

        self.results = {}

    def _run_model(self, name: str, model):
        model.fit(self.train_data, self.train_labels)
        predictions = model.predict(self.test_data)
        metrics = Metrics(self.test_labels, predictions, self.label_names, name)
        self.results[name] = metrics

    def _log_model(self, name: str, model: Any, config: dict, model_tags: Dict[str, str], save_model: bool = False):
        with mlflow.start_run():
            mlflow.log_params(self.dataset_chars)

            if 'base_model' in config:
                mlflow.log_param('meta_model', config['model_type'])
                mlflow.log_params(config['base_model'])
            else:
                mlflow.log_params(config)

            mlflow.log_metrics(self.results[name].metrics)
            if model_tags:
                mlflow.set_tags(model_tags)

            if save_model:
                if isinstance(model, BaseEstimator):
                    mlflow.sklearn.log_model(model, artifact_path="models/" + name, registered_model_name=name)
                elif isinstance(model, nn.Module):
                    mlflow.pytorch.log_model(model, artifact_path="models/" + name, registered_model_name=name)
                else:
                    print(f"Model type not supported for automatic MLflow logging: {type(model)}")

    def run_experiment(self, models: Dict[str, Any], configs: Dict[str, Any], mlflow_path: Optional[str] = None,
                       tags: Dict[str, Dict[str, str]] = None, save_models: bool = False):

        if models.keys() != configs.keys():
            print('Non-matching keys in `models` and `configs` input dictionaries. Please provide dictionaries with'
                  ' corresponding keys')
            return

        if mlflow_path:
            mlflow.set_experiment(mlflow_path)

        for name, model in models.items():
            self._run_model(name, model)
            model_tags = tags.get(name, {})
            self._log_model(name, model, configs[name], model_tags, save_models)
