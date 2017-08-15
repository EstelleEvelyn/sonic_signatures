from double_bayes import DoubleBayes
import itertools
import numpy as np
import matplotlib.pyplot as plt
from naive_bayes import Naive_Bayes
from sklearn import svm, datasets
from sklearn.metrics import confusion_matrix


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Gender Classification',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def get_confusion_matrix():
#    db = DoubleBayes()
#    predicted, actual = db.generate_predictions(weighted=True)
    nb = Naive_Bayes()
    predicted, actual = nb.generate_predictions()
    cnf_matrix = confusion_matrix(actual, predicted)
    return cnf_matrix

def main():
#    class_names = ["Other Characters", "Protagonists", "Antagonists", "Fool"]
    class_names = ["Female", "Male"]
    cnf_matrix = get_confusion_matrix()
    np.set_printoptions(precision=2)
    plt.figure()
    plot_confusion_matrix(cnf_matrix, classes=class_names)
    plt.show()

if __name__ == "__main__":
    main()
