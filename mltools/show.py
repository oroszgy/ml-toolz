import itertools

import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

from mltools.metrics import accuracy_confidence_interval, accuracy_p_value, precision_at_k_simple


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          size=(20, 20),
                          x_rotation=45,
                          cmap=None):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    import matplotlib.pyplot as plt

    cmap = cmap or plt.cm.Blues

    plt.figure(figsize=size)
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=x_rotation)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def print_confusion_matrix(cm, labels, hide_zeroes=False, hide_diagonal=False, hide_threshold=None):
    columnwidth = max([len(str(x)) for x in labels] + [5])  # 5 is value length
    empty_cell = " " * columnwidth
    print("    " + empty_cell, end=" ")
    for label in labels:
        print("%{0}s".format(columnwidth) % label, end=" ")
    print()
    for i, label1 in enumerate(labels):
        print("    %{0}s".format(columnwidth) % label1, end=" ")
        for j in range(len(labels)):
            cell = "%{0}d".format(columnwidth) % cm[i, j]
            if hide_zeroes:
                cell = cell if float(cm[i, j]) != 0 else empty_cell
            if hide_diagonal:
                cell = cell if i != j else empty_cell
            if hide_threshold:
                cell = cell if cm[i, j] > hide_threshold else empty_cell
            print(cell, end=" ")
        print()


def print_classification_pipeline_scores(y_test, y_pred, y_score=None, labels=None, confidence_level=0.9,
                                         show_topk=False, show_cm=False):
    print("=== Test results ===")
    print("Accuracy: {:.2f}%".format(accuracy_score(y_test, y_pred) * 100))
    lower_acc, upper_acc = accuracy_confidence_interval(y_test, y_pred, confidence_level)
    print("Accuracy confidence intervals: {:.2f} and {:.2f} with {:.2f} level".format(lower_acc * 100, upper_acc * 100,
                                                                                      confidence_level))
    print("Accuracy p-value: {:.4f}".format(accuracy_p_value(y_test, y_pred)))

    if show_topk:
        print()
        assert y_score is not None
        assert labels is not None
        print("Precision@3: {:.2f}%".format(
            precision_at_k_simple(y_test, y_score, labels, k=3) * 100))
        print("Precision@5: {:.2f}%".format(
            precision_at_k_simple(y_test, y_score, labels, k=5) * 100))

    print()
    print("Classification report")
    print(classification_report(y_test, y_pred))

    if show_cm:
        print()
        print("Confusion matrix")
        assert labels is not None
        cm = confusion_matrix(y_test, y_pred, labels)
        print_confusion_matrix(cm, labels=labels)
