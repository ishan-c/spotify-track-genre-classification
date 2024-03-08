"""
This module provides the `Metrics` class, with functionality to calculate and display metrics for evaluating multi-label
classification models.

It supports the calculation of Hamming Loss, Jaccard Score (with weighted averaging), and detailed classification
reports including precision, recall, F1 scores (macro, micro, and weighted averages), and support for each label.

The module is designed to handle multi-label classification tasks (thought it should be able to handle binary and
multi-class classification as well) and provides methods to print aggregated metrics as well as  per-label metrics.
"""

import numpy as np
import pandas as pd
from scipy.sparse import lil_matrix
from sklearn.metrics import classification_report, hamming_loss, jaccard_score


class Metrics:
    """
    A class to compute, store, and display metrics for various multi-label classification models

    Parameters:
    - y_true (np.ndarray): ground truth binary labels array, shape (n_samples, n_labels).
    - y_pred (lil_matrix): predicted labels as a  sparse matrix, shape (n_samples, n_labels).
    - labels (list): label names corresponding to columns in `y_true` and `y_pred`.

    Attributes:
    - hamming (float): Hamming loss for the predictions.
    - jaccard (float): weighted average Jaccard score for the predictions.
    - headers (str): header section of the classification report provided by sklearn
    - label_report (str): per-label metrics section of the classification report.
    - global_report (str): global metrics section of the classification report.

    Methods:
    - print_metrics(): prints the global performance metrics (Hamming Loss and Jaccard Score) and aggregated label
        metrics
    - print_label_metrics(n_labels=None): prints metrics for each label. If `n_labels` is specified, only metrics for
        the top `n_labels` are printed.
    """

    def __init__(self, y_true: np.ndarray, y_pred: lil_matrix, labels: pd.Series):
        """
        Initializes the Metrics object with true labels, predicted labels, and label names, and computes initial metrics

        Parameters:
        - y_true (np.ndarray): ground truth binary labels array of shape (n_samples, n_labels).
        - y_pred (lil_matrix): predicted labels as a dense or sparse matrix of shape (n_samples, n_labels).
        - labels (pd.Series): label names corresponding to columns in `y_true` and `y_pred`.
        """

        self.y_true = y_true
        self.y_pred = y_pred

        self.headers, self.label_report, self.global_report = self._parse_report(labels.tolist())
        self.jaccard = jaccard_score(y_true, y_pred, average='weighted', zero_division=0)
        self.hamming = hamming_loss(y_true, y_pred)

    def _parse_report(self, labels: list) -> tuple:
        """
        Internal method to parse the classification report into its constituent parts.

        Parameters:
        - labels (list): A list of label names.

        Returns:
        - tuple: Contains the headers, label-specific report, and global metrics report as strings.
        """
        report = classification_report(y_true=self.y_true, y_pred=self.y_pred, target_names=labels, digits=3, zero_division=0)
        report_sections = report.split('\n\n')

        return report_sections[0], report_sections[1], report_sections[2]

    def print_metrics(self):
        """
        Prints the overall metrics including Hamming Loss and Jaccard Score, along with the global model performance.
        """
        print(f'Hamming Loss: {self.hamming:.4f}')
        print(f'Jaccard Score (Weighted Avg): {self.jaccard:.4f}')
        print(self.headers + '\n' + self.global_report)

    def print_label_metrics(self, n_labels: int = None):
        """
        Prints metrics for individual labels. If `n_labels` is specified, limits the output to the top `n_labels`.

        Parameters:
        - n_labels (int), optional: number of label metrics to print. If not provided, prints metrics for all labels
        """
        report = self.headers + '\n' + self.label_report

        if n_labels:
            lines = report.split('\n')
            if 0 < n_labels <= len(lines) - 1:
                report = '\n'.join(lines[:n_labels + 1])
            else:
                print('Requested value of `n_labels` is out of bounds, providing all label metrics:')

        print('Label level metrics:\n' + report)
