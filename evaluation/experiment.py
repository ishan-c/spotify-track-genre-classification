"""
This module provides an Experiment class for managing model experiments and logging using MLflow.
It facilitates the training, evaluation, and logging of models along with their configurations and performance metrics.
Supports logging of different model types, including scikit-learn estimators and PyTorch models, with flexibility
to add custom tags for detailed experiment tracking.
"""
from typing import Any, Dict, List, Optional

import mlflow
import numpy as np
import torch.nn as nn
from sklearn.base import BaseEstimator

from evaluation.metrics import Metrics


class Experiment:
    """
    Manages experiments, including model training, evaluation, and logging to MLflow.

    Attributes:
        train_data (np.ndarray): training data features
        train_labels (np.ndarray): training data labels
        test_data (np.ndarray): test data features
        test_labels (np.ndarray): test data labels
        dataset_chars (dict): characteristics of the dataset used for the experiment, used for logging
        label_names (List[str]): names of the labels for the experiment
        models (dict): stores model instances provided to the experiment
        results (dict): stores metrics of each model run within the experiment
    """

    def __init__(self, train_data: np.ndarray, train_labels: np.ndarray, test_data: np.ndarray, test_labels: np.ndarray,
                 dataset_chars: dict):
        self.train_data = train_data
        self.train_labels = train_labels
        self.test_data = test_data
        self.test_labels = test_labels
        self.dataset_chars = dataset_chars
        self.label_names = dataset_chars['labels']

        self.models = {}
        self.results = {}

    def _run_model(self, name: str, model):
        """
       Fits the model with training data and predicts on test data. Stores metrics in the results dictionary.

       Parameters:
           name (str): user-provided model name
           model: model instance used for training, prediction, and evaluation
       """

        model.fit(self.train_data, self.train_labels)
        predictions = model.predict(self.test_data)
        metrics = Metrics(self.test_labels, predictions, self.label_names, name)
        self.results[name] = metrics

    def _log_model_run(self, name: str, model: Any, config: dict, model_tags: Dict[str, str], save_model: bool = False):
        """
        Logs model configuration, metrics, and optionally the model itself to MLflow

        Parameters:
            name (str): model name provided by user
            model: the machine learning model instance to be logged
            config (dict): configuration parameters of the model
            model_tags (dict): optional custom tags to add to the MLflow log for this model
            save_model (bool): if True, the model will be saved to MLflow, otherwise only metrics and params are logged
        """

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
                    mlflow.sklearn.log_model(model, artifact_path='/models/' + name, registered_model_name=name)
                elif isinstance(model, nn.Module):
                    mlflow.pytorch.log_model(model, artifact_path='/models/' + name, registered_model_name=name)
                else:
                    print(f"Model type not supported for automatic MLflow logging: {type(model)}")

    def run_experiment(self, models: Dict[str, Any], configs: Dict[str, Any], mlflow_path: Optional[str] = None,
                       tags: Dict[str, Dict[str, str]] = None, save_models: bool = False):
        """
        Executes the experiment with provided models, configurations, and additional parameters. Logs results to MLflow

        Parameters:
            models (dict): model names and their corresponding instances
            configs (dict):  model names and their corresponding configurations
            mlflow_path (str, optional): path name of the MLflow experiment under which to log this run
            tags (dict): optional, model names and their corresponding tag dictionaries for logging
            save_models (bool): whether to save the trained model to MLflow. If True, models are logged
        """

        if models.keys() != configs.keys():
            print('Non-matching keys in `models` and `configs` input dictionaries. Please provide dictionaries with'
                  ' corresponding keys')
            return

        if mlflow_path:
            mlflow.set_experiment(mlflow_path)

        self.models = models

        for name, model in self.models.items():
            print(f'Running model: {name}')
            self._run_model(name, model)
            model_tags = tags.get(name, {})
            self._log_model_run(name, model, configs[name], model_tags, save_models)
            print(f'{name} complete.')
