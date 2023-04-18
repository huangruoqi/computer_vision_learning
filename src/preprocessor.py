import os
import pickle

import numpy
from collections import Counter
from tsa import helper as hlp
from tsa import augmentation as aug


class Preprocessor:
    def transform(self, data):
        raise Exception("<transform> method must be defined for Preprocessor")

    def __str__(self):
        raise Exception("<__str__> method must be defined for Preprocessor")


class PCA(Preprocessor):
    def __init__(self):
        self.pca = None
        from sklearn.decomposition import PCA

        try:
            pardir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), os.path.pardir)
            )
            pca_file = open(os.path.join(pardir, "pca.pkl"), "rb")
            self.pca = pickle.load(pca_file)
            pca_file.close()
        except Exception as e:
            print(e)
            print("PCA not loaded")
            pass

    def transform(self, data):
        x, y = data
        if self.pca is not None:
            x = [[v for k, v in enumerate(i) if k % 4 != 3] for i in x]
            x = self.pca.transform(x)
        return x, y

    def __str__(self):
        return "Principle Component Analysis"


class RemoveVisibility(Preprocessor):
    def transform(self, data):
        x, y = data
        if self.pca is not None:
            x = [[v for k, v in enumerate(i) if k % 4 != 3] for i in x]
        return x, y

    def __str__(self):
        return "Remove Visibility"

class Balancer(Preprocessor):
    def __init__(self, threshold, ratio):
        self.threshold = threshold
        self.ratio = ratio

    def transform(self, data):
        x, y = data
        label = None
        count = 0
        x_temp = []
        y_temp = []
        x_result = []
        y_result = []
        for i in range(len(x)):
            if y[i] == label:
                count += 1
            else:
                label = y[i]
                count = 0
                x_result.extend(x_temp)
                y_result.extend(y_temp)
                x_temp = []
                y_temp = []
            x_temp.append(x[i])
            y_temp.append(y[i])
            if count >= self.threshold:
                count = 0
                label = None
                x_result.extend(x_temp[:self.threshold//self.ratio])
                y_result.extend(y_temp[:self.threshold//self.ratio])
                x_temp = []
                y_temp = []
        
        if len(x_temp):
            x_result.extend(x_temp)
            y_result.extend(y_temp)

        print(Counter(y_result))

        return x_result, y_result

    def __str__(self):
        return "Balance Input"

class Augmentation(Balancer):
    def __init__(self):
        super().__init__(100, 10)

    def _get_minority(self, data):
        x, y = data
        most_common = Counter(y).most_common()[0][0]
        self.threshold
        for i in range(len(x)):
            if y[i]!=most_common:
                pass

        return data


    
class Jitter(Augmentation):
    def transform(self, data):
        data = super().transform(data)
        if len(data[0])==0:
            return data
        minority = self._get_minority(data)
        # x = aug.jitter(x)
        # s = numpy.swapaxes(numpy.array(x), 1, 0)
        # hlp.plot1d(s[0])
        return data