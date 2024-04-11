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

baseline_rf_50_est_experiment_configs = [
    {
        'model_type': 'skmultilearn.problem_transform.BinaryRelevance',
        'base_model': {
            'model_type': 'sklearn.ensemble.RandomForestClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'n_estimators': 50
            }
        }

    },
    {
        'model_type': 'skmultilearn.problem_transform.ClassifierChain',
        'base_model': {
            'model_type': 'sklearn.ensemble.RandomForestClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'n_estimators': 50
            }
        }
    },
    {
        'model_type': 'skmultilearn.problem_transform.LabelPowerset',
        'base_model': {
            'model_type': 'sklearn.ensemble.RandomForestClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'n_estimators': 50
            }
        }
    }
]

baseline_rf_15_depth_experiment_configs = [
    {
        'model_type': 'skmultilearn.problem_transform.BinaryRelevance',
        'base_model': {
            'model_type': 'sklearn.ensemble.RandomForestClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'max_depth': 15
            }
        }

    },
    {
        'model_type': 'skmultilearn.problem_transform.ClassifierChain',
        'base_model': {
            'model_type': 'sklearn.ensemble.RandomForestClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'max_depth': 15
            }
        }
    },
    {
        'model_type': 'skmultilearn.problem_transform.LabelPowerset',
        'base_model': {
            'model_type': 'sklearn.ensemble.RandomForestClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'max_depth': 15
            }
        }
    }
]

baseline_rf_50_est_15_depth_experiment_configs = [
    {
        'model_type': 'skmultilearn.problem_transform.BinaryRelevance',
        'base_model': {
            'model_type': 'sklearn.ensemble.RandomForestClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'n_estimators': 50,
                'max_depth': 15
            }
        }

    },
    {
        'model_type': 'skmultilearn.problem_transform.ClassifierChain',
        'base_model': {
            'model_type': 'sklearn.ensemble.RandomForestClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'n_estimators': 50,
                'max_depth': 15
            }
        }
    },
    {
        'model_type': 'skmultilearn.problem_transform.LabelPowerset',
        'base_model': {
            'model_type': 'sklearn.ensemble.RandomForestClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'n_estimators': 50,
                'max_depth': 15
            }
        }
    }
]

baseline_rf_10_est_15_depth_experiment_configs = [
    {
        'model_type': 'skmultilearn.problem_transform.BinaryRelevance',
        'base_model': {
            'model_type': 'sklearn.ensemble.RandomForestClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'n_estimators': 10,
                'max_depth': 15
            }
        }

    },
    {
        'model_type': 'skmultilearn.problem_transform.ClassifierChain',
        'base_model': {
            'model_type': 'sklearn.ensemble.RandomForestClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'n_estimators': 10,
                'max_depth': 15
            }
        }
    },
    {
        'model_type': 'skmultilearn.problem_transform.LabelPowerset',
        'base_model': {
            'model_type': 'sklearn.ensemble.RandomForestClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'n_estimators': 10,
                'max_depth': 15
            }
        }
    }
]

baseline_rf_50_est_10_depth_experiment_configs = [
    {
        'model_type': 'skmultilearn.problem_transform.BinaryRelevance',
        'base_model': {
            'model_type': 'sklearn.ensemble.RandomForestClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'n_estimators': 50,
                'max_depth': 10
            }
        }

    },
    {
        'model_type': 'skmultilearn.problem_transform.ClassifierChain',
        'base_model': {
            'model_type': 'sklearn.ensemble.RandomForestClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'n_estimators': 50,
                'max_depth': 10
            }
        }
    },
    {
        'model_type': 'skmultilearn.problem_transform.LabelPowerset',
        'base_model': {
            'model_type': 'sklearn.ensemble.RandomForestClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'n_estimators': 50,
                'max_depth': 10
            }
        }
    }
]

baseline_rf_10_est_10_depth_experiment_configs = [
    {
        'model_type': 'skmultilearn.problem_transform.BinaryRelevance',
        'base_model': {
            'model_type': 'sklearn.ensemble.RandomForestClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'n_estimators': 10,
                'max_depth': 10
            }
        }

    },
    {
        'model_type': 'skmultilearn.problem_transform.ClassifierChain',
        'base_model': {
            'model_type': 'sklearn.ensemble.RandomForestClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'n_estimators': 10,
                'max_depth': 10
            }
        }
    },
    {
        'model_type': 'skmultilearn.problem_transform.LabelPowerset',
        'base_model': {
            'model_type': 'sklearn.ensemble.RandomForestClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'n_estimators': 10,
                'max_depth': 10
            }
        }
    }
]

baseline_gb_0_05_lr_200_est_experiment_configs = [
    {
        'model_type': 'skmultilearn.problem_transform.BinaryRelevance',
        'base_model': {
            'model_type': 'sklearn.ensemble.GradientBoostingClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'learning_rate': 0.05,
                'n_estimators': 200
            }
        }

    },
    {
        'model_type': 'skmultilearn.problem_transform.ClassifierChain',
        'base_model': {
            'model_type': 'sklearn.ensemble.GradientBoostingClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'learning_rate': 0.05,
                'n_estimators': 200
            }
        }
    },
    {
        'model_type': 'skmultilearn.problem_transform.LabelPowerset',
        'base_model': {
            'model_type': 'sklearn.ensemble.GradientBoostingClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'learning_rate': 0.05,
                'n_estimators': 200
            }
        }
    }
]

baseline_gb_0_2_lr_50_est_experiment_configs = [
    {
        'model_type': 'skmultilearn.problem_transform.BinaryRelevance',
        'base_model': {
            'model_type': 'sklearn.ensemble.GradientBoostingClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'learning_rate': 0.2,
                'n_estimators': 50
            }
        }

    },
    {
        'model_type': 'skmultilearn.problem_transform.ClassifierChain',
        'base_model': {
            'model_type': 'sklearn.ensemble.GradientBoostingClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'learning_rate': 0.2,
                'n_estimators': 50
            }
        }
    },
    {
        'model_type': 'skmultilearn.problem_transform.LabelPowerset',
        'base_model': {
            'model_type': 'sklearn.ensemble.GradientBoostingClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'learning_rate': 0.2,
                'n_estimators': 50
            }
        }
    }
]

baseline_gb_0_05_lr_500_est_experiment_configs = [
    {
        'model_type': 'skmultilearn.problem_transform.BinaryRelevance',
        'base_model': {
            'model_type': 'sklearn.ensemble.GradientBoostingClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'learning_rate': 0.05,
                'n_estimators': 500
            }
        }

    },
    {
        'model_type': 'skmultilearn.problem_transform.ClassifierChain',
        'base_model': {
            'model_type': 'sklearn.ensemble.GradientBoostingClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'learning_rate': 0.05,
                'n_estimators': 500
            }
        }
    },
    {
        'model_type': 'skmultilearn.problem_transform.LabelPowerset',
        'base_model': {
            'model_type': 'sklearn.ensemble.GradientBoostingClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'learning_rate': 0.05,
                'n_estimators': 500
            }
        }
    }
]

baseline_gb_0_03_lr_500_est_experiment_configs = [
    {
        'model_type': 'skmultilearn.problem_transform.BinaryRelevance',
        'base_model': {
            'model_type': 'sklearn.ensemble.GradientBoostingClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'learning_rate': 0.03,
                'n_estimators': 500
            }
        }

    },
    {
        'model_type': 'skmultilearn.problem_transform.ClassifierChain',
        'base_model': {
            'model_type': 'sklearn.ensemble.GradientBoostingClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'learning_rate': 0.03,
                'n_estimators': 500
            }
        }
    },
    {
        'model_type': 'skmultilearn.problem_transform.LabelPowerset',
        'base_model': {
            'model_type': 'sklearn.ensemble.GradientBoostingClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'learning_rate': 0.03,
                'n_estimators': 500
            }
        }
    }
]

baseline_gb_0_01_lr_500_est_experiment_configs = [
    {
        'model_type': 'skmultilearn.problem_transform.BinaryRelevance',
        'base_model': {
            'model_type': 'sklearn.ensemble.GradientBoostingClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'learning_rate': 0.01,
                'n_estimators': 500
            }
        }

    },
    {
        'model_type': 'skmultilearn.problem_transform.ClassifierChain',
        'base_model': {
            'model_type': 'sklearn.ensemble.GradientBoostingClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'learning_rate': 0.01,
                'n_estimators': 500
            }
        }
    },
    {
        'model_type': 'skmultilearn.problem_transform.LabelPowerset',
        'base_model': {
            'model_type': 'sklearn.ensemble.GradientBoostingClassifier',
            'hyperparameters': {
                'random_state': SEED,
                'learning_rate': 0.01,
                'n_estimators': 500
            }
        }
    }
]
