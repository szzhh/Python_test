# UML Data Mining Project
name: Yibiao Wu
ID: 01502319

To test Decision Tree:  

python main.py -m 0

To test Random Forest:  

python main.py -m 1

### Description of the Code

#### Decision Tree Class
#### *Creating a Decision Tree*
1. The train(self) function is the entry point to the creation of a decision tree. It handles the selection of random attributes to build the tree on and the calling of tree_growth() function.

#with two members
a.root: to store the root node
b.and attribute: to marked attributes that used for building decision tree

#Extract data with needed attributes and attached labels to each record new_records = [] for r in records:     new = []     for atr in attributes:         new.append(r["attributes"][atr])     new.append(r["label"])     new_records.append(new)  # grow the tree self.root = self.tree_growth(new_records) return self.root


2. The tree_growth(self, records, attributes) function recursively builds the decision tree by splitting on select attributes by way of entropy.

for col in range(0, column_count):     # Generate the list of all possible different values in the considered column     # Added for debugging     global column_values     column_values = {}     for row in records:         column_values[row[col]] = 1     # Now try dividing the rows up for each value in this column     for value in column_values.keys():         # the 'values' here are the keys of the dictionary         (set1, set2) = self.divideset(records, col, value)         # define set1 and set2 as the 2 children set of a division          # Information gain         p = float(len(set1)) / len(records)         # p is the size of a child set relative to its parent          gain = current_score - p * self.entropy(set1) - (1 - p) * self.entropy(set2)          if gain > best_gain and len(set1) > 0 and len(set2) > 0:             # set must not be empty             best_gain = gain             best_criteria = (col, value)             best_sets = (set1, set2)

3.prediction. This function will go through the tree from the root to the leaf node
def predict(self,sample):     """     This function predicts the label of given sample     ""     branch = self
    #go through the tree till reach leaf note     while branch.results == None:          if sample[branch.col] == branch.value:             # True Branch             branch = branch.tb          else:             # False Branch             branch = branch.fb      # Once you reach the leaf, return the classification label     return branch.results.keys()[0]


###RandomForest
#### *Creating a Random Forest*
1. The Random Forest Class first produces the bootstrap samples by gathering the same number of samples as the size of the provided data set:

	python
         bootstrap(self, records):     """     This function bootstrap will return a set of records, which has the same     size with the original records but with replacement.     """     sample = list()     for i in range(1, len(records)):         sample.append(records[random.randint(0, len(records) - 1)])


	

2. Using this bootstrap sample set, the Random Forest class then creates a DecisionTree() with it and adds the tree to the forest:

m = 6 forest = list() for i in range(self.tree_num):     new_records = self.bootstrap(records)     sub_attributes = random.sample(attributes, m)     sorted_sub_attributes = sorted(sub_attributes)     dt = DecisionTree()     dt.train(new_records, attributes)     forest.append(dt)  self.forest = forest return forest

	

3. Steps 1 & 2 are repeated for the number of requested trees (self.tree_num) in the forest.


#### *Prediction with a Random Forest*

	predictions = [] for tree in self.forest:     predictions.append(tree.predict(sample)) #return the label that get the most notes. return max(set(predictions), key=predictions.count)

	



	
	
  
  
*Reference site for a Decision Tree in Python:*
http://www.patricklamle.com/Tutorials/Decision%20tree%20python/tuto_decision%20tree.html

