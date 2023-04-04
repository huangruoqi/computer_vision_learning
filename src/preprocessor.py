import os
import pickle


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
        if self.pca is not None:
            data = [[v for k, v in enumerate(i) if k % 4 != 3] for i in data]
            data = self.pca.transform(data)
        return data

    def __str__(self):
        return "Principle Component Analysis"


class RemoveVisibility(Preprocessor):
    def transform(self, data):
        return [[v for k, v in enumerate(i) if k % 4 != 3] for i in data]

    def __str__(self):
        return "Remove Visibility"
