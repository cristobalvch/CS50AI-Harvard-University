import csv
import sys
import numpy as np 

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier




TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    MONTH = {'Jan':0,'Feb':1,'Mar':2,'Apr':3,
             'May':4,'June':5,'Jul':6,'Aug':7,
             'Sep':8,'Oct':9,'Nov':10,'Dec':11}
    WEEKEND = {'FALSE':0, 'TRUE':1}
    REVENUE = {'FALSE':0 ,'TRUE':1}

    evidence = []
    labels = []

    with open(filename, 'r', newline='') as file:
        data = csv.reader(file)
        next(data)
        for col in data:
            col[1] = float(col[1])
            col[3] = float(col[3])
            col[5:10] = [float(col[i]) for i in range(5, 10)]

            col[10] = MONTH[col[10]]

            if col[15] == 'Returning_Visitor':
                col[15] = 1
            else:
                col[15] = 0

            col[16] = WEEKEND[col[16]]

            col[-1] = REVENUE[col[-1]]

            evidence.append(col[:-1])
            labels.append(col[-1])

    evidence = np.array(evidence).astype(np.float32)
    labels = np.array(labels).astype(np.float32)

    return (evidence, labels)


def train_model(X_train, y_train):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(X_train, y_train)

    return model 


def evaluate(y_test, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    labels_arrays = np.array(y_test)
    preds_array = np.array(predictions)

    positives = sum(labels_arrays)
    correct_positives = sum(labels_arrays*preds_array)
    sensitivity = correct_positives /  positives

    negatives = len(labels_arrays) - positives
    incorret_negatives = len(labels_arrays) - np.count_nonzero(labels_arrays+preds_array)
    specificity = incorret_negatives / negatives
    
        


    return sensitivity, specificity


if __name__ == "__main__":
    main()