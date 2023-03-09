import pandas as pd
import os
import sys
import numpy as np

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from label_config import LABELS
labels2int = {b:a for a, b in enumerate(LABELS)}

landmark_indices = [
    0, 11, 12, 13, 14, 15, 16, 23, 24
]
# convert landmarks to only selected landmarks
def convert(landmarks):
    result = []
    for index in landmark_indices:
        landmark = landmarks[index]
        result.extend([landmark.x, landmark.y, landmark.z, landmark.visibility])
    return result

# offset according to previous frame
def offset(curr, prev):
    result = [(v[0] - v[1]) if i&3!=3 else v[0] for i, v in enumerate(zip(curr, prev))]
    # print(sum([v for i, v in enumerate(result) if i&3!=3]))
    return result

def convert_df_labels(df1, labels2int):
    df = df1.copy()
    for i in range(len(df)):
        label = df['label'][i]
        df.at[i, 'label'] = labels2int[label]
    return df


def split_data_with_label(df, valid_size, test_size):
    df_input = df.copy()
    df_target = df_input.pop('label')
    groups = {}
    current_group_label = None
    current_group = []
    for i, row in enumerate(df_input.itertuples(index=False)):
        if current_group_label is None:
            current_group_label = df_target[i]
        if current_group_label == df_target[i]:
            current_group.append(row)
        else:
            groups[current_group_label] = groups.get(current_group_label, [])
            groups[current_group_label].append(current_group)
            current_group_label = df_target[i]
            current_group = []
    if len(current_group):
        groups[current_group_label] = groups.get(current_group_label, [])
        groups[current_group_label].append(current_group)

    x_train, x_valid, x_test = [], [], []
    y_train, y_valid, y_test = [], [], []
    for label, group in groups.items():
        # random.shuffle(group)
        combined = [j for i in group for j in i]
        n_test = int(len(combined) * test_size)
        n_valid = int(len(combined) * valid_size)
        n_train = len(combined) - n_test - n_valid
        for i in range(len(combined)):
            (x_train if i < n_train else x_valid if i < n_train+n_valid else x_test).append(combined[i])
            (y_train if i < n_train else y_valid if i < n_train+n_valid else y_test).append(label)
    return np.array(x_train), np.array(y_train),np.array(x_valid), np.array(y_valid),np.array(x_test), np.array(y_test)
    
def split_data_without_label(df, valid_size, test_size):
    df_input = df.copy()
    df_target = df_input.pop('label')
    x_train, x_valid, x_test = [], [], []
    y_train, y_valid, y_test = [], [], []
    n_test = int(len(df_input) * test_size)
    n_valid = int(len(df_input) * valid_size)
    n_train = len(df_input) - n_test - n_valid
    for i, row in enumerate(df_input.itertuples(index=False)):
        (x_train if i < n_train else x_valid if i < n_train+n_valid else x_test).append(row)
        (y_train if i < n_train else y_valid if i < n_train+n_valid else y_test).append(df_target[i])
    return x_train, y_train,x_valid, y_valid,x_test, y_test
    

def split_data(DATA, VALID_RATIO, TEST_RATIO):
    DBs = [pd.read_csv(os.path.join("data", f"{name}.csv"), index_col=0) for name in DATA]
    DB = pd.concat(DBs, axis=0, ignore_index=True, sort=False)
    DB = convert_df_labels(DB, labels2int)

    return split_data_without_label(DB, VALID_RATIO, TEST_RATIO)

def save_model_info(model_type, file_path, model_path, model_acc):
    dst = os.path.join(model_path, 'info.txt')
    src_file = open(file_path, 'r')
    content = src_file.read().split("#MODEL_INFO")
    src_file.close()
    assert len(content) == 3
    model_info = content[1]
    with open(dst, 'w') as f:
        f.write(f"Model type: {model_type}\n")
        f.write(f"Model accuracy: {'{:.3f}%'.format(model_acc*100)}\n\n")
        f.write("--- MODEL INFO ---")
        f.write(model_info)
    src = 'label_config.py'
    dst = os.path.join(model_path, 'label_config.py')
    src_file = open(src, 'r')
    content = src_file.read().split("#LABEL")
    src_file.close()
    assert len(content) == 2
    label_info = content[1]
    with open(dst, 'w') as f:
        f.write(label_info)

def group_data(data, group_size):
    result = []
    temp = []
    for i in data:
        temp.append(i)
        if len(temp)==group_size:
            result.append(temp)
            temp = []

    return np.array(result)

def group_data_score(data, group_size):
    result = []
    temp = []
    for i in data:
        temp.append(i)
        if len(temp)==group_size:
            result.append(sum(temp)/16/2)
            temp = []

    return np.array(result)
