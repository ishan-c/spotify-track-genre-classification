import numpy as np
import pandas as pd
from scipy.sparse import lil_matrix
from sklearn.metrics import classification_report, hamming_loss, jaccard_score


class Metrics:
    def __init__(self, y_true: np.ndarray, y_pred: lil_matrix, labels: pd.Series):
        self.y_true = y_true
        self.y_pred = y_pred

        self.headers, self.label_report, self.global_report = self._parse_report(labels.tolist())
        self.jaccard = jaccard_score(y_true, y_pred, average='weighted', zero_division=0)
        self.hamming = hamming_loss(y_true, y_pred)

    def _parse_report(self, labels: list):
        report = classification_report(y_true=self.y_true, y_pred=self.y_pred, target_names=labels, digits=3, zero_division=0)
        report_sections = report.split('\n\n')

        return report_sections[0], report_sections[1], report_sections[2]

    def print_metrics(self):
        print(f'Hamming Loss: {self.hamming}')
        print(f'Jaccard Score (Weighted Avg): {self.jaccard}')
        print(self.headers + '\n' + self.global_report)

    def print_label_metrics(self, n_labels: int = None):
        report = self.headers + '\n' + self.label_report

        if n_labels:
            lines = report.split('\n')
            if 0 < n_labels <= len(lines) - 1:
                report = '\n'.join(lines[:n_labels + 1])
            else:
                print('Requested value of `n_labels` is out of bounds, providing all label metrics:')

        print(report)
