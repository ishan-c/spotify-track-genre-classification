import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


def scale_numeric_data(train_array: np.ndarray, test_array: np.ndarray, feature_names: list,
                       scaled_feature_names: list = None) -> tuple:

    scaler = StandardScaler()
    train_df = pd.DataFrame(train_array, columns=feature_names)
    test_df = pd.DataFrame(test_array, columns=feature_names)

    if scaled_feature_names is None:
        scaled_feature_names = ['duration_ms', 'tempo', 'loudness']

    train_df[scaled_feature_names] = scaler.fit_transform(train_df[scaled_feature_names])
    test_df[scaled_feature_names] = scaler.transform(test_df[scaled_feature_names])

    return train_df.to_numpy(), test_df.to_numpy()
