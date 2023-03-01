from __future__ import print_function


class TreeNode(object):
    def __init__(self, isLeaf=False, col=None, value=None, results=None, tb=None, fb=None):
        # Your code here
        self.col = col
        self.value = value
        self.results = results
        self.tb = tb
        self.fb = fb

    def predict(self,sample):
        """
        This function predicts the label of given sample
        """
        # Your code here
        # Is this a leaf node?
        branch = self

        while branch.results == None:
            if sample[branch.col] == branch.value:
                # True Branch
                branch = branch.tb

            else:
                # False Branch
                branch = branch.fb

        # Once you reach the leaf, return the classification label
        return branch.results.keys()[0]




class DecisionTree(object):
    """
    Class of the Decision Tree
    """

    def __init__(self):
        self.root = None
        self.attributes = None

    def train(self, records, attributes):
        """
        This function trains the model with training records "records" and
        attribute set "attributes", the format of the data is as follows:
            records: training records, each record contains following fields:
                label - the lable of this record
                attributes - a list of attribute values
            attributes: a list of attribute indices that you can use for
                        building the tree
        Typical data will look like:
            records: [
                        {
                            "label":"p",
                            "attributes":['p','x','y',...]
                        },
                        {
                            "label":"e",
                            "attributes":['b','y','y',...]
                        },
                        ...]
            attributes: [0, 2, 5, 7,...]

        """
        # Store attributes that used for building the tree
        self.attributes = attributes

        # Extract data with needed attributes and attached labels to each record
        new_records = []
        for r in records:
            new = []
            for atr in attributes:
                new.append(r["attributes"][atr])
            new.append(r["label"])
            new_records.append(new)

        # grow the tree
        self.root = self.tree_growth(new_records)
        return self.root

    def predict(self, sample):
        """
        This function predict the label for new sample by calling the predict
        function of the root node
        """

        # Extract data with needed attributes from sample
        newSample = []
        for atr in self.attributes:
            newSample.append(sample["attributes"][atr])

        return self.root.predict(newSample)

    def divideset(self, rows, column, value):
        # Make a function that tells us if a row is in the first group(true) or the second
        # group(false)
        split_function = None
        split_function = lambda row: row[column] == value

        # Divide the rows into two sets and return them
        set1 = [row for row in rows if split_function(row)]
        set2 = [row for row in rows if not split_function(row)]
        return (set1, set2)

        # Create counts of possible results (the last column of each row is the result)

    def uniquecounts(self, rows):
        results = {}
        for row in rows:
            # The result is the last column
            r = row[len(row) - 1]
            if r not in results: results[r] = 0
            results[r] += 1
        return results

        # Entropy is the sum of p(x)log(p(x)) across all
        # the different possible results

    def entropy(self, rows):
        from math import log
        log2 = lambda x: log(x) / log(2)
        results = self.uniquecounts(rows)
        # Now calculate the entropy
        ent = 0.0
        for r in results.keys():
            p = float(results[r]) / len(rows)
            ent = ent - p * log2(p)
        return ent

    def tree_growth(self, records):
        """
        This function grows the Decision Tree recursively until the stopping
        criterion is met. Please see textbook p164 for more details

        This function should return a TreeNode
        """
        # Your code here
        # Hint-1: Test whether the stopping criterion has been met by calling function stopping_cond()
        # Hint-2: If the stopping criterion is met, you may need to create a leaf node
        # Hint-3: If the stopping criterion is not met, you may need to create a
        #         TreeNode, then split the records into two parts and build a
        #         child node for each part of the subset

        # stopping criterion 1: out of data
        if len(records) == 0:
            return TreeNode()
        # len(rows) is the number of units in a set
        current_score = self.entropy(records)

        # Set up some variables to track the best criteria
        best_gain = 0.0
        best_criteria = None
        best_sets = None

        column_count = len(records[0]) - 1
        # count the # of attributes/columns.
        # It's -1 because the last one is the target attribute and it does not count.

        for col in range(0, column_count):
            # Generate the list of all possible different values in the considered column
            # Added for debugging
            global column_values
            column_values = {}
            for row in records:
                column_values[row[col]] = 1
            # Now try dividing the rows up for each value in this column
            for value in column_values.keys():
                # the 'values' here are the keys of the dictionary
                (set1, set2) = self.divideset(records, col, value)
                # define set1 and set2 as the 2 children set of a division

                # Information gain
                p = float(len(set1)) / len(records)
                # p is the size of a child set relative to its parent

                gain = current_score - p * self.entropy(set1) - (1 - p) * self.entropy(set2)

                if gain > best_gain and len(set1) > 0 and len(set2) > 0:
                    # set must not be empty
                    best_gain = gain
                    best_criteria = (col, value)
                    best_sets = (set1, set2)

        # Create the sub branches: right branch and left branch
        if best_gain > 0:
            trueBranch = self.tree_growth(best_sets[0])
            falseBranch = self.tree_growth(best_sets[1])
            return TreeNode(col=best_criteria[0], value=best_criteria[1],
                                tb=trueBranch, fb=falseBranch)
        else:
            # stopping criterion 2: when the gain is not going up
            return TreeNode(results=self.uniquecounts(records))

    def printtree(self, tree, indent=' ', sample = None):
        # Is this a leaf node?
        if tree.results is not None:
            print(str(tree.results))
        else:
            print(str(tree.col) + ':' + str(tree.value) + '? ')
            # Print the branches
            print(indent + 'T->', end = " ")
            self.printtree(tree.tb, indent + "  ", sample)
            print(indent + 'F->', end = " ")
            self.printtree(tree.fb, indent + "  ", sample)

