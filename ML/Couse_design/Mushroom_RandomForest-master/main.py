import argparse

from DecisionTree import DecisionTree
from RandomForest import RandomForest


def load_data(file_path):
    """
    Load data from given file path, please see data description for details
    of the data format
    """
    records = []
    file = open(file_path)
    for line in file:
        tokens = line.strip().split(',')
        records.append({"label": tokens[0], "attributes": tokens[1:]})
    attributes = range(len(records[0]["attributes"]))
    file.close()
    return records, attributes


def test_model(model, training_file_path, testing_file_path):
    """
    Test the accuracy of given model
    """
    records, attributes = load_data(training_file_path)
    model.train(records, attributes)
    test_records = load_data(testing_file_path)[0]

    correct_cnt = 0
    for sample in test_records:
        if model.predict(sample) == sample["label"]:
            correct_cnt += 1

    print "Accuracy:", float(correct_cnt) / len(test_records)




def main():

    #Process the input arguments

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', default="0")
    parser.add_argument('-t', '--training', default="data/mushrooms_train.data")
    parser.add_argument('-e', '--testing', default="data/mushrooms_test.data")
    parser.add_argument('-d', '--max_depth', default=10)
    parser.add_argument('-n', '--tree_nums', default=4)
    args = parser.parse_args()

    if args.model == "0":
        print "Testing Decision Tree model"
        model = DecisionTree()
    else:
        print "Testing Random Forest model"
        model = RandomForest(args.tree_nums)

    test_model(model, args.training, args.testing)

if __name__ == "__main__":
    main()
