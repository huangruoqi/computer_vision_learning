import pickle
from numpy import array
from sklearn.decomposition import PCA

from mutils import split_data, group_data, group_data_score, labels2int, save_model_info

# Don't remove the comment below
# MODEL_INFO
MODEL_NAME = "Score"
DATA = [
    "1676842496.mp4",
    "1676842883.mp4",
    "1676843917.mp4",
    "1676842689.mp4",
]
VALID_RATIO = 0.1
TEST_RATIO = 0.1

x_train, y_train, x_valid, y_valid, x_test, y_test = split_data(
    DATA, VALID_RATIO, TEST_RATIO
)
# define a matrix
A = array(x_train)
# create the PCA instance
pca = PCA(0.9)
# fit on data
pca.fit(A)
print(pca.n_components_)
print(pca.explained_variance_)
# transform data
B = pca.transform(A)
# print(B)
with open("pca.pkl", "wb") as pickle_file:
    pickle.dump(pca, pickle_file)
