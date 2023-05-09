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
        index = 0
        while index < len(x):
            if y[index] == label:
                count += 1
            else:
                label = y[index]
                count = 1
                x_result.extend(x_temp)
                y_result.extend(y_temp)
                x_temp = []
                y_temp = []
            x_temp.append(x[index])
            y_temp.append(y[index])
            if count >= self.threshold:
                count = 0
                label = None
                index+=1
                while index < len(x):
                    if y[index] == label:
                        index+=1
                        x_temp.append(x[index])
                        y_temp.append(y[index])
                    else:
                        break
                x_result.extend(x_temp[::self.ratio])
                y_result.extend(y_temp[::self.ratio])
                x_temp = []
                y_temp = []
            index += 1
        
        if len(x_temp):
            x_result.extend(x_temp)
            y_result.extend(y_temp)
        return x_result, y_result

    def __str__(self):
        return "Balance Input"

class Augmentation(Balancer):
    def __init__(self):
        super().__init__(200, 50)

    def _get_minority(self, data):
        x, y = data
        most_common = Counter(y).most_common()[0][0]
        index = 0
        padding = self.threshold//self.ratio
        x_result = []
        y_result = []
        while index < len(x):
            if y[index]!=most_common:
                start = max(0, index - padding)
                end = start + 1
                while end < len(x) and y[end]!=most_common:
                    end += 1
                end = min(len(x)-1, end + padding)
                x_result.extend(x[start:end+1])
                y_result.extend(y[start:end+1])
                index = end
            index += 1
        return x_result, y_result


    
class Jitter(Augmentation):
    def transform(self, data):
        data = super().transform(data)
        x_result, y_result = [], []
        if len(data[0])==0:
            return data
        x, y = self._get_minority(data)
        for i in range(2):
            x_j = aug.jitter(numpy.array(x))
            x_result.extend(x_j)
            y_result.extend(y)
        x_result.extend(data[0])
        y_result.extend(data[1])
        print(Counter(y_result))
        return data

    def __str__(self):
        return "Jitter"

class StableFilter(Preprocessor):
    def __init__(self, stable_label, padding):
        self.stable_label = stable_label
        self.padding = padding

    def transform(self, data):
        x_result = []
        x, y = data
        n = len(x)
        forward, backward = [0]*n, [0]*n
        f_count, b_count = 0, 0
        for i in range(n):
            if y[i]!=self.stable_label:
                forward[i] = 1
                f_count = self.padding
            elif f_count > 0:
                forward[i] = 1
                f_count -= 1
            if y[n-i-1]!=self.stable_label:
                backward[n-i-1] = 1
                b_count = self.padding
            elif b_count > 0:
                backward[n-i-1] = 1
                b_count -= 1
        for i in range(n):
            if forward[i]==1 or backward[i]==1:
                pass
            else:
                x_result.append(x[i])
        return x_result, x_result

    def __str__(self):
        return "Stable Filter"


class UnstableFilter(Preprocessor):
    def __init__(self, stable_label, padding):
        self.stable_label = stable_label
        self.padding = padding

    def transform(self, data):
        x_result = []
        x, y = data
        n = len(x)
        forward, backward = [0]*n, [0]*n
        f_count, b_count = 0, 0
        for i in range(n):
            if y[i]!=self.stable_label:
                forward[i] = 1
                f_count = self.padding
            elif f_count > 0:
                forward[i] = 1
                f_count -= 1
            if y[n-i-1]!=self.stable_label:
                backward[n-i-1] = 1
                b_count = self.padding
            elif b_count > 0:
                backward[n-i-1] = 1
                b_count -= 1
        for i in range(n):
            if forward[i]==1 or backward[i]==1:
                x_result.append(x[i])
            else:
                pass
        return x_result, x_result

    def __str__(self):
        return "Unstable Filter"
