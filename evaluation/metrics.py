"""
This module provides the `Metrics` class, with functionality to calculate and display metrics for evaluating multi-label
classification models.

It supports the calculation of Hamming Loss, Jaccard Score (with weighted averaging), and detailed classification
reports including precision, recall, F1 scores (macro, micro, and weighted averages), and support for each label.

The module is designed to handle multi-label classification tasks (thought it should be able to handle binary and
multi-class classification as well) and provides methods to print aggregated metrics as well as  per-label metrics.
"""
from typing import Optional

import numpy as np
from scipy.sparse import lil_matrix
from sklearn.metrics import classification_report, hamming_loss, jaccard_score, precision_recall_fscore_support


class Metrics:
    """
    A class to compute, store, and display metrics for various multi-label classification models

    Parameters:
    - y_true (np.ndarray): ground truth binary labels array, shape (n_samples, n_labels)
    - y_pred (lil_matrix): predicted labels as a  sparse matrix, shape (n_samples, n_labels)
    - labels (list): label names corresponding to columns in `y_true` and `y_pred`
    - name (str): optional name associating metrics to a model or model run

    Attributes:
    - metrics (dict): flat dictionary containing all metrics
    - headers (str): header section of the classification report provided by sklearn
    - label_report (str): per-label metrics section of the classification report
    - global_report (str): global metrics section of the classification report

    Methods:
    - get_metrics(): returns dictionary containing all calculated metrics
    - print_metrics_report(): prints the global performance metrics (Hamming Loss and Jaccard Score) and aggregated
        label metrics
    - print_label_metrics_report(n_labels=None): prints metrics for each label. If `n_labels` is specified, only metrics
        for the top `n_labels` are printed.
    """

    def __init__(self, y_true: np.ndarray, y_pred: lil_matrix, labels: list, name: Optional[str] = None):
        """
        Initializes the Metrics object with true labels, predicted labels, and label names, and computes initial metrics

        Parameters:
        - y_true (np.ndarray): ground truth binary labels array of shape (n_samples, n_labels).
        - y_pred (lil_matrix): predicted labels as a dense or sparse matrix of shape (n_samples, n_labels).
        - labels (list): label names corresponding to columns of `y_true` and `y_pred`.
        - name (str, optional): optional argument to associate metrics with a model or run
        """

        self.y_true = y_true
        self.y_pred = y_pred
        self.name = name
        self.metrics = None

        report = self._calculate_metrics(labels)
        self.headers, self.label_report, self.global_report = self._parse_report(report)

    def _calculate_metrics(self, labels: list):
        """
        Internal method to call the necessary metric functions from scikit-learn

        Parameters:
        - labels (list): list of label names.

        Returns:
        - report (str): output of the scikit-learn classification report, parsed later by _parse_report() method
        """

        jaccard = jaccard_score(self.y_true, self.y_pred, average='weighted', zero_division=0)
        hamming = hamming_loss(self.y_true, self.y_pred)
        precision_mi, recall_mi, f1_mi, _ = precision_recall_fscore_support(self.y_true, self.y_pred, average='micro',
                                                                            zero_division=0)
        precision_ma, recall_ma, f1_ma, _ = precision_recall_fscore_support(self.y_true, self.y_pred, average='macro',
                                                                            zero_division=0)
        precision_wt, recall_wt, f1_wt, _ = precision_recall_fscore_support(self.y_true, self.y_pred,
                                                                            average='weighted', zero_division=0)
        precision_sa, recall_sa, f1_sa, _ = precision_recall_fscore_support(self.y_true, self.y_pred, average='samples',
                                                                            zero_division=0)

        self.metrics = {
            'weighted_jaccard': jaccard,
            'hamming_loss': hamming,
            'precision_micro_avg': precision_mi,
            'recall_micro_avg': recall_mi,
            'f1_micro_avg': f1_mi,
            'precision_macro_avg': precision_ma,
            'recall_macro_avg': recall_ma,
            'f1_macro_avg': f1_ma,
            'precision_weighted_avg': precision_wt,
            'recall_weighted_avg': recall_wt,
            'f1_weighted_avg': f1_wt,
            'precision_samples_avg': precision_sa,
            'recall_samples_avg': recall_sa,
            'f1_samples_avg': f1_sa
        }

        report = classification_report(y_true=self.y_true, y_pred=self.y_pred, target_names=labels, digits=3,
                                       zero_division=0)

        return report

    def get_metrics(self) -> dict:
        """
        Provides all metrics associated with run in dictionary format

        Returns:
        - dict: `metrics` attribute, the dictionary containing all stored metrics for model run
        """
        return self.metrics

    @staticmethod
    def _parse_report(report: str) -> tuple:
        """
        Internal method to parse the classification report into its constituent parts.

        Parameters:
        - report (str): str containing the output report from scikit classification_report
        - labels (list): list of label names.

        Returns:
        - tuple: Contains the headers, label-specific report, and global metrics report as strings.
        """

        report_sections = report.split('\n\n')

        return report_sections[0], report_sections[1], report_sections[2]

    def print_metrics_report(self):
        """
        Prints the overall metrics including Hamming Loss and Jaccard Score, along with the global model performance.
        """
        print(f'Hamming Loss: {self.metrics["hamming_loss"]:.4f}')
        print(f'Jaccard Score (Weighted Avg): {self.metrics["weighted_jaccard"]:.4f}')
        print(self.headers + '\n' + self.global_report)

    def print_label_metrics_report(self, n_labels: int = None):
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
