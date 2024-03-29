from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import itertools
import numpy as np

#%%
def plot_confusion_matrix(y_true, y_pred,
                          classes=None,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.

        args:
            y_true: list of true labels
            y_pred: list of predicted labels
            classes: list of class names
            normalize: boolean, if True, normalize the confusion matrix
            title: title of the plot
            cmap: color map of the plot

        returns:
            cm: confusion matrix
    """
    if classes is None:
        classes = np.unique(y_true)
    cm = confusion_matrix(y_true, y_pred, labels=classes)
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=90)
    plt.yticks(tick_marks, classes)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            text = f".{cm[i,j]*100:.0f}"
        else:
            text = f"{cm[i, j]}"
        plt.text(j, i, text,
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True')
    plt.xlabel('Predicted')
    plt.show()

    return cm