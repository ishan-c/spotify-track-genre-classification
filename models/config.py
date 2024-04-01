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
