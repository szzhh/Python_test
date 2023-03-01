import random
from DecisionTree import DecisionTree

class RandomForest(object):
    """
    Class of the Random Forest
    """

    def __init__(self, tree_num):
        self.tree_num = tree_num
        self.forest = []

    def train(self, records, attributes):
        """
        This function will train the random forest, the basic idea of training a
        Random Forest is as follows:
        1. Draw n bootstrap samples using bootstrap() function
        2. For each of the bootstrap samples, grow a tree with a subset of
            original attributes, which is of size m (m << # of total attributes)
        """
        # n_trees is the number of the tree
        # Your code here
        # I set m = 6 as default
        m = 6
        forest = list()
        for i in range(self.tree_num):
            new_records = self.bootstrap(records)
            sub_attributes = random.sample(attributes, m)
            sorted_sub_attributes = sorted(sub_attributes)
            dt = DecisionTree()
            dt.train(new_records, attributes)
            forest.append(dt)

        self.forest = forest
        return forest

    def predict(self, sample):
        """
        The predict function predicts the label for new data by aggregating the
        predictions of each tree.

        This function should return the predicted label
        """

        # Your code here
        predictions = []
        for tree in self.forest:
            predictions.append(tree.predict(sample))
        #return the label that get the most notes.
        return max(set(predictions), key=predictions.count)

    def bootstrap(self, records):
        """
        This function bootstrap will return a set of records, which has the same
        size with the original records but with replacement.
        """
        sample = list()
        for i in range(1, len(records)):
            sample.append(records[random.randint(0, len(records) - 1)])

        return sample

