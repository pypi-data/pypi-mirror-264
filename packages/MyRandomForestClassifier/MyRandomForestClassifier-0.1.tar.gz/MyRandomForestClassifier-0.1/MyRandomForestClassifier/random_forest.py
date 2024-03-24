from decision_tree import DecisionTree
import numpy as np
from collections import Counter
from multiprocessing import Pool

class MyRandomForestClassifier:
    def __init__(
        self,
        n_estimators=100,
        max_depth=100,
        min_samples_split=2,
        n_features=None,
        criterion='entropy',
        n_jobs=None
    ):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.n_features = n_features
        self.criterion = criterion
        self.n_jobs = n_jobs
        self.trees = []

    def fit(self, X, y):
        with Pool(processes=self.n_jobs) as pool:
            results = pool.starmap(self._fit_tree, [(X, y) for _ in range(self.n_estimators)])
        self.trees = results

    def _fit_tree(self, X, y):
        tree = DecisionTree(
            max_depth=self.max_depth,
            min_samples_split=self.min_samples_split,
            n_features=self.n_features,
            criterion=self.criterion
        )
        x_sample, y_sample = self._bootstrap_sample(X, y)
        tree.fit(x_sample, y_sample)
        return tree

    def predict(self, X):
        with Pool(processes=self.n_jobs) as pool:
            predictions = pool.starmap(self._predict_tree, [(tree, X) for tree in self.trees])
        predictions = np.array(predictions)
        tree_predictions = np.swapaxes(predictions, 0, 1)
        predictions = np.array([self._most_common_label(pred) for pred in tree_predictions])
        return predictions

    def _predict_tree(self, tree, X):
        return tree.predict(X)

    def _bootstrap_sample(self, X, y):
        n_samples = X.shape[0]
        sample_indices = np.random.choice(n_samples, n_samples, replace=True)
        return X[sample_indices], y[sample_indices]

    def _most_common_label(self, y):
        counter = Counter(y)
        most_common = counter.most_common(1)[0][0]
        return most_common