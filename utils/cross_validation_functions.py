from evaluation.experiment import Experiment
from models.setup import experiment_setup
from utils.dataset import Dataset
from utils.scaling import scale_numeric_data


def build_cv_experiments(n_splits: int, dataset: Dataset, random_state=42):
    train_data, train_labels, _, test_data, test_labels, _ = dataset.split_data(cross_val=True, n_splits=n_splits,
                                                                                iterative=True,
                                                                                random_state=random_state,
                                                                                force_split=True)

    fold_experiments = []
    for i in range(n_splits):
        train_data[i], test_data[i] = scale_numeric_data(train_data[i], test_data[i], dataset.feature_names)
        fold_characteristics = dataset.get_dataset_characteristics(i)
        fold_experiment = Experiment(train_data[i], train_labels[i], test_data[i], test_labels[i], fold_characteristics)
        fold_experiments.append(fold_experiment)

    return fold_experiments


def run_cv_experiments(experiments, experiment_configs, mlflow_path, model_names, tags, save_models, log_results):
    for i, experiment in enumerate(experiments):
        fold_names = [model_name + f'_{i + 1}' for model_name in model_names]
        fold_tags = {model_name + f'_{i + 1}': tags[model_name] for model_name in model_names}
        for model_name in fold_tags:
            fold_tags[model_name]['Fold'] = f'{i + 1} / {len(experiments)}'

        fold_models, fold_configs = experiment_setup(experiment_configs, fold_names)
        experiment.run_experiment(fold_models, fold_configs, mlflow_path, fold_tags, save_models=save_models,
                                  log_results=log_results)


def average_cv_metrics(experiments, model_name_root):
    sum_metrics = None
    for i, experiment in enumerate(experiments):
        fold_model_name = model_name_root + f'_{i + 1}'
        fold_metrics = experiment.results[fold_model_name].metrics
        if sum_metrics is None:
            sum_metrics = fold_metrics.copy()
        else:
            for key in sum_metrics.keys():
                sum_metrics[key] += fold_metrics[key]

    return {key: float(f'{value / len(experiments):.3f}') for key, value in sum_metrics.items()}
