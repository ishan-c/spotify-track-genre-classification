from pathlib import Path

import pickle


def save_experiments(experiments, experiment_path: Path, filename: str):
    filename = filename + '.pkl' if filename[-4:] != '.pkl' else filename
    with open(experiment_path / filename, 'wb') as f:
        pickle.dump(experiments, f)


def load_experiments(experiment_path: Path, name: str):
    filename = name + '.pkl' if name[-4:] != '.pkl' else name
    with open(experiment_path / filename, 'rb') as f:
        experiments = pickle.load(f)
    return experiments
