import numpy as np
from collections import Counter
from multiprocessing import Pool

class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, *, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

    def is_leaf_node(self):
        return self.value is not None

class DecisionTree:
    def __init__(self, criterion="entropy", min_samples_split=2, max_depth=100, n_features=None):
        self.criterion = criterion
        self.min_samples_split = min_samples_split
        self.max_depth = max_depth
        self.n_features = n_features
        self.root = None

    def fit(self, X, y):
        self.n_features = X.shape[1] if not self.n_features else min(X.shape[1], self.n_features)
        self.root = self._grow_tree(X, y)

    def _grow_tree(self, X, y, depth=0):
        n_samples, n_feats = X.shape
        n_labels = len(np.unique(y))

        if depth >= self.max_depth or n_labels == 1 or n_samples < self.min_samples_split:
            leaf_value = self._most_common_label(y)
            return Node(value=leaf_value)

        feat_idxs = np.random.choice(n_feats, self.n_features, replace=False)
        best_feature, best_thresh = self._best_split(X, y, feat_idxs)
        left_idxs, right_idxs = self._split(X[:, best_feature], best_thresh)
        left = self._grow_tree(X[left_idxs, :], y[left_idxs], depth + 1)
        right = self._grow_tree(X[right_idxs, :], y[right_idxs], depth + 1)
        return Node(best_feature, best_thresh, left, right)
    
    def _best_split(self, X, y, feat_idxs):
        return self._best_split_entropy(X, y, feat_idxs)

    def _best_split_gini(self, x, y, feat_idxs):
        max_gini_gain = -np.inf
        best_feature, best_threshold = None, None
        for feature in feat_idxs:
            x_column = x[:, feature]
            thresholds = np.unique(x_column)
            for thres in thresholds:
                gini_gain = self._gini_gain(y, x_column, thres)
                if gini_gain > max_gini_gain:
                    max_gini_gain = gini_gain
                    best_feature = feature
                    best_threshold = thres
        return best_feature, best_threshold

    def _best_split_entropy(self, X, y, feat_idxs):
        best_feat, best_thresh = None, None
        best_gain = -1
        for feat in feat_idxs:
            x_column = X[:, feat]
            thresholds = np.unique(x_column)
            gains = self._information_gain_vectorized(y, x_column, thresholds)
            best_idx = np.argmax(gains)
            if gains[best_idx] > best_gain:
                best_gain = gains[best_idx]
                best_feat = feat
                best_thresh = thresholds[best_idx]
        return best_feat, best_thresh

    def _most_common_label(self, y):
        counter = Counter(y)
        value = counter.most_common(1)[0][0]
        return value

    def _split(self, X_column, split_thresh):
        left_idxs = np.argwhere(X_column <= split_thresh).flatten()
        right_idxs = np.argwhere(X_column > split_thresh).flatten()
        return left_idxs, right_idxs

    def _gini(self, y):
        unique_labels, counts = np.unique(y, return_counts=True)
        probabilities = counts / len(y)
        gini = 1 - np.sum(probabilities ** 2)
        return gini

    def _gini_gain(self, y, x_column, threshold):
        parent_gini = self._gini(y)
        left_idxs, right_idxs = self._split(x_column, threshold)
        if len(left_idxs) == 0 or len(right_idxs) == 0:
            return 0
        n = len(y)
        n_l, n_r = len(left_idxs), len(right_idxs)
        left_gini = self._gini(y[left_idxs])
        right_gini = self._gini(y[right_idxs])
        gini_gain = parent_gini - (n_l / n) * left_gini - (n_r / n) * right_gini
        return gini_gain

    def _information_gain_vectorized(self, y, x_column, thresholds):
        parent_entropy = self._entropy(y)
        n = len(y)
        gains = []
        for threshold in thresholds:
            left_idxs = x_column <= threshold
            right_idxs = x_column > threshold
            n_l, n_r = np.sum(left_idxs), np.sum(right_idxs)
            if n_l == 0 or n_r == 0:
                gains.append(0)
                continue
            left_entropy = self._entropy(y[left_idxs])
            right_entropy = self._entropy(y[right_idxs])
            ig = parent_entropy - (n_l / n) * left_entropy - (n_r / n) * right_entropy
            gains.append(ig)
        return np.array(gains)

    def _entropy(self, y):
        _, counts = np.unique(y, return_counts=True)
        probabilities = counts / len(y)
        entropy = -np.sum(probabilities * np.log2(probabilities))
        return entropy

    def predict(self, X):
        return np.array([self._traverse_tree(x, self.root) for x in X])

    def _traverse_tree(self, x, node):
        if node.is_leaf_node():
            return node.value
        if x[node.feature] <= node.threshold:
            return self._traverse_tree(x, node.left)
        return self._traverse_tree(x, node.right)

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