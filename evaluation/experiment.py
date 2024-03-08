from evaluation.metrics import Metrics


class Experiment:
    def __init__(self, models: dict):
        self.classifiers = models
        self.results = {}

    def run_experiment(self, X_train, y_train, X_test, y_test, labels):

        for name, model in self.classifiers.items():
            print(f'Training {name}...')
            _ = model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            metrics = Metrics(y_test, predictions, labels)
            self.results[name] = metrics
            print(f'Results for {name}:')
            metrics.print_metrics()

    def get_metrics(self, classifier_name: str):

        return self.results.get(classifier_name)
