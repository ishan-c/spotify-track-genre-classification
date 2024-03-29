import importlib

META_MODELS = ['BinaryRelevance', 'ClassifierChain', 'LabelPowerset']


def _create_model(config: dict):
    module_name, class_name = config['model_type'].rsplit('.', 1)
    module = importlib.import_module(module_name)
    model_class = getattr(module, class_name)

    if class_name in META_MODELS:
        base_model = _create_model(config['base_model'])
        model = model_class(classifier=base_model, **config.get('hyperparameters', {}))
    else:
        model = model_class(**config.get('hyperparameters', {}))

    return model


def experiment_setup(model_configs: list, names: list = None):
    models = {}
    configs = {}

    for i, config in enumerate(model_configs):
        if names and len(names) == len(model_configs):
            name = names[i]
        else:
            name = config['model_type'].split('.')[-1]
        models[name] = _create_model(config)
        configs[name] = config

    return models, configs
