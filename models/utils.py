import importlib

META_MODELS = ['BinaryRelevance', 'ClassifierChain', 'LabelPowerset']


def create_model(config):
    module_name, class_name = config['model_type'].rsplit('.', 1)
    module = importlib.import_module(module_name)
    model_class = getattr(module, class_name)

    if class_name in META_MODELS:
        base_model = create_model(config['base_model'])
        model = model_class(classifier=base_model, **config.get('hyperparameters', {}))
    else:
        model = model_class(**config.get('hyperparameters', {}))

    return model
