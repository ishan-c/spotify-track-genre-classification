from typing import Optional, Tuple

import mlflow
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from skmultilearn.model_selection import IterativeStratification


class Dataset:
    """

    """
    def __init__(self, input_data: pd.DataFrame, feature_names: list, label_names: list, id_column_name: str):
        self.df = input_data

        if id_column_name not in input_data.columns:
            raise ValueError(f"Input data does not contain a column named: {id_column_name}")

        missing_features = [f for f in feature_names if f not in input_data.columns]
        missing_labels = [l for l in label_names if l not in input_data.columns]
        if missing_features or missing_labels:
            raise ValueError(f':Input column names are missing in the input data: {missing_features + missing_labels}')

        self.feature_names = feature_names
        self.n_features = len(feature_names)
        self.features = self.df[feature_names].to_numpy()

        self.label_names = label_names
        self.n_labels = len(label_names)
        self.labels = self.df[label_names].to_numpy()

        self.ids = self.df[id_column_name].to_numpy()
        self.n_examples = len(self.ids)

        self.split_complete = False
        self.random_state = None
        self.n_train_examples = None
        self.n_test_examples = None

        self.log_complete = False

    def split_data(self, test_size: float, iterative: bool = True, random_state: [int, float] = None,
                   force_split: bool = False) -> Optional[Tuple[np.ndarray, np.ndarray, np.ndarray,
                                                          np.ndarray, np.ndarray, np.ndarray]]:
        """

        """
        if not (0 < test_size < 1):
            print('Please choose `test_size` between 0 and 1, non-inclusive.')
            return
        if self.split_complete:
            print('Dataset has already been split, proceeding will overwrite split data. Continue? (Y/N)')
            if force_split:
                print('`force_split`=True, Proceeding with new split.')
                pass
            else:
                print('Canceling split.')
                return

        if iterative:
            x_train, y_train, ids_train, x_test, y_test, ids_test = self._iterative_train_test_split(test_size)
        else:
            x_train, y_train, ids_train, x_test, y_test, ids_test = self._train_test_split(test_size, random_state)

        self.random_state = random_state
        self.n_train_examples = len(ids_train)
        self.n_test_examples = len(ids_test)
        self.split_complete = True

        return x_train, y_train, ids_train, x_test, y_test, ids_test

    def _iterative_train_test_split(self, test_size: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray,
                                                                     np.ndarray, np.ndarray, np.ndarray]:

        """

        """
        stratifier = IterativeStratification(n_splits=2, order=2, sample_distribution_per_fold=[test_size,
                                                                                                1.0 - test_size])
        train_indexes, test_indexes = next(stratifier.split(self.features, self.labels))

        features_train, labels_train, ids_train = self.features[train_indexes, :], self.labels[train_indexes, :], \
            self.ids[train_indexes]
        features_test, labels_test, ids_test = self.features[test_indexes, :], self.labels[test_indexes, :], \
            self.ids[test_indexes]

        return features_train, labels_train, ids_train, features_test, labels_test, ids_test

    def _train_test_split(self, test_size: float, random_state):
        """

        """
        features_train, labels_train,ids_train, features_test, labels_test, ids_test = \
            train_test_split(self.features, self.labels, self.ids, test_size=test_size, random_state=random_state)
        return features_train, labels_train, ids_train, features_test, labels_test, ids_test

    def log_dataset(self, force_log: bool = False):
        """

        """
        if not self.split_complete:
            print('This dataset has not yet been split. Please call split_data() first in order to obtain train and '
                  'test sizes for logs.')
            return
        if self.log_complete:
            print('Dataset has already been logged.')
            if force_log:
                print('`force_log` = True, Proceeding with logging.')
                pass
            else:
                print('Canceling logging.')
                return

        dataset_characteristics = {
            'features': self.feature_names,
            'labels': self.label_names,
            'n_features': self.n_features,
            'n_labels': self.n_labels,
            'random_state': self.random_state,
            'n_examples': self.n_examples,
            'n_train_examples': self.n_train_examples,
            'n_test_examples': self.n_test_examples
        }

        with mlflow.start_run():
            mlflow.log_params(dataset_characteristics)

        self.log_complete = True

        return
