SEED = 42

baseline_experiment_configs = [
    {
        'model_type': 'skmultilearn.problem_transform.BinaryRelevance',
        'base_model': {
            'model_type': 'sklearn.linear_model.LogisticRegression',
            'hyperparameters': {
                'max_iter': 1000,
                'random_state': SEED
            }
        }

    },
    {
        'model_type': 'skmultilearn.problem_transform.ClassifierChain',
        'base_model': {
            'model_type': 'sklearn.linear_model.LogisticRegression',
            'hyperparameters': {
                'max_iter': 1000,
                'random_state': SEED
            }
        }

    },
    {
        'model_type': 'skmultilearn.problem_transform.LabelPowerset',
        'base_model': {
            'model_type': 'sklearn.linear_model.LogisticRegression',
            'hyperparameters': {
                'max_iter': 1000,
                'random_state': SEED
            }
        }
    }
]

baseline_0_1_C_experiment_configs = [
    {
        'model_type': 'skmultilearn.problem_transform.BinaryRelevance',
        'base_model': {
            'model_type': 'sklearn.linear_model.LogisticRegression',
            'hyperparameters': {
                'max_iter': 1000,
                'random_state': SEED,
                'C': 0.1
            }
        }

    },
    {
        'model_type': 'skmultilearn.problem_transform.ClassifierChain',
        'base_model': {
            'model_type': 'sklearn.linear_model.LogisticRegression',
            'hyperparameters': {
                'max_iter': 1000,
                'random_state': SEED,
                'C': 0.1
            }
        }
    },
    {
        'model_type': 'skmultilearn.problem_transform.LabelPowerset',
        'base_model': {
            'model_type': 'sklearn.linear_model.LogisticRegression',
            'hyperparameters': {
                'max_iter': 1000,
                'random_state': SEED,
                'C': 0.1
            }
        }
    }
]

baseline_10_C_experiment_configs = [
    {
        'model_type': 'skmultilearn.problem_transform.BinaryRelevance',
        'base_model': {
            'model_type': 'sklearn.linear_model.LogisticRegression',
            'hyperparameters': {
                'max_iter': 1000,
                'random_state': SEED,
                'C': 10.0
            }
        }

    },
    {
        'model_type': 'skmultilearn.problem_transform.ClassifierChain',
        'base_model': {
            'model_type': 'sklearn.linear_model.LogisticRegression',
            'hyperparameters': {
                'max_iter': 1000,
                'random_state': SEED,
                'C': 10.0
            }
        }
    },
    {
        'model_type': 'skmultilearn.problem_transform.LabelPowerset',
        'base_model': {
            'model_type': 'sklearn.linear_model.LogisticRegression',
            'hyperparameters': {
                'max_iter': 1000,
                'random_state': SEED,
                'C': 10.0
            }
        }
    }
]

baseline_100_C_experiment_configs = [
    {
        'model_type': 'skmultilearn.problem_transform.BinaryRelevance',
        'base_model': {
            'model_type': 'sklearn.linear_model.LogisticRegression',
            'hyperparameters': {
                'max_iter': 1000,
                'random_state': SEED,
                'C': 100.0
            }
        }

    },
    {
        'model_type': 'skmultilearn.problem_transform.ClassifierChain',
        'base_model': {
            'model_type': 'sklearn.linear_model.LogisticRegression',
            'hyperparameters': {
                'max_iter': 1000,
                'random_state': SEED,
                'C': 100.0
            }
        }
    },
    {
        'model_type': 'skmultilearn.problem_transform.LabelPowerset',
        'base_model': {
            'model_type': 'sklearn.linear_model.LogisticRegression',
            'hyperparameters': {
                'max_iter': 1000,
                'random_state': SEED,
                'C': 100.0
            }
        }
    }
]

baseline_saga_10_C_experiment_configs = [
    {
        'model_type': 'skmultilearn.problem_transform.BinaryRelevance',
        'base_model': {
            'model_type': 'sklearn.linear_model.LogisticRegression',
            'hyperparameters': {
                'max_iter': 1000,
                'random_state': SEED,
                'C': 10.0,
                'solver': 'saga'
            }
        }

    },
    {
        'model_type': 'skmultilearn.problem_transform.ClassifierChain',
        'base_model': {
            'model_type': 'sklearn.linear_model.LogisticRegression',
            'hyperparameters': {
                'max_iter': 1000,
                'random_state': SEED,
                'C': 10.0,
                'solver': 'saga'
            }
        }
    },
    {
        'model_type': 'skmultilearn.problem_transform.LabelPowerset',
        'base_model': {
            'model_type': 'sklearn.linear_model.LogisticRegression',
            'hyperparameters': {
                'max_iter': 1000,
                'random_state': SEED,
                'C': 10.0,
                'solver': 'saga'
            }
        }
    }
]

baseline_linearsvc_experiment_configs = [
    {
        'model_type': 'skmultilearn.problem_transform.BinaryRelevance',
        'base_model': {
            'model_type': 'sklearn.svm.LinearSVC',
            'hyperparameters': {
                'max_iter': 1000,
                'random_state': SEED
            }
        }

    },
    {
        'model_type': 'skmultilearn.problem_transform.ClassifierChain',
        'base_model': {
            'model_type': 'sklearn.svm.LinearSVC',
            'hyperparameters': {
                'max_iter': 1000,
                'random_state': SEED
            }
        }
    },
    {
        'model_type': 'skmultilearn.problem_transform.LabelPowerset',
        'base_model': {
            'model_type': 'sklearn.svm.LinearSVC',
            'hyperparameters': {
                'max_iter': 1000,
                'random_state': SEED
            }
        }
    }
]

baseline_random_forest_experiment_configs = [
    {
        'model_type': 'skmultilearn.problem_transform.BinaryRelevance',
        'base_model': {
            'model_type': 'sklearn.ensemble.RandomForestClassifier',
            'hyperparameters': {
                'random_state': SEED
            }
        }

    },
    {
        'model_type': 'skmultilearn.problem_transform.ClassifierChain',
        'base_model': {
            'model_type': 'sklearn.ensemble.RandomForestClassifier',
            'hyperparameters': {
                'random_state': SEED
            }
        }
    },
    {
        'model_type': 'skmultilearn.problem_transform.LabelPowerset',
        'base_model': {
            'model_type': 'sklearn.ensemble.RandomForestClassifier',
            'hyperparameters': {
                'random_state': SEED
            }
        }
    }
]

baseline_gradient_boost_experiment_configs = [
    {
        'model_type': 'skmultilearn.problem_transform.BinaryRelevance',
        'base_model': {
            'model_type': 'sklearn.ensemble.GradientBoostingClassifier',
            'hyperparameters': {
                'random_state': SEED
            }
        }

    },
    {
        'model_type': 'skmultilearn.problem_transform.ClassifierChain',
        'base_model': {
            'model_type': 'sklearn.ensemble.GradientBoostingClassifier',
            'hyperparameters': {
                'random_state': SEED
            }
        }
    },
    {
        'model_type': 'skmultilearn.problem_transform.LabelPowerset',
        'base_model': {
            'model_type': 'sklearn.ensemble.GradientBoostingClassifier',
            'hyperparameters': {
                'random_state': SEED
            }
        }
    }
]
