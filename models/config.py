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
