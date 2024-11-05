from CN2Unordered import CN2Unordered
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import argparse
import re
import time
from Evaluator import Evaluator
from tqdm import tqdm


# Funzione di convalida personalizzata
def param_discr(param):
    pattern = r"^(cut|qcut)_[0-9]+$"
    if not re.match(pattern, param):
        raise argparse.ArgumentTypeError("Parameter format is not valid")
    return param

def param_eval_func(param):
    if param not in Evaluator.get_menu():
        raise argparse.ArgumentTypeError("Parameter format is not valid")
    return param

def gtzan_ex(max_star_size, max_rules, evaluation_func, discr):
    labels_dict = {
                  2: ["low", "high"],
                  3: ["low", "medium", "high"],
                  4: ["very low", "low", "high", "very high"],
                  5: ["very low", "low", "medium", "high", "very high"],
    }


    general_path = './gtzan'
    data_30 = pd.read_csv(f'{general_path}/features_30_sec.csv')
    data_3 = pd.read_csv(f'{general_path}/features_3_sec.csv')

    discr = discr.split('_')
    discr = (pd.cut,'raise',int(discr[1])) if discr[0]=='cut' else (pd.qcut,'drop', int(discr[1]))
    data = data_30
    data = data.iloc[0:, 1:]
    print(data.columns)
    for feature in data.columns[1:-1]:
        print(discr, len(labels_dict[discr[2]]))
        #data[feature] = discr[0](data[feature], discr[2], duplicates=discr[1])
        data[feature] = discr[0](data[feature], discr[2], labels=labels_dict[discr[2]], duplicates=discr[1])
        print(data[feature].value_counts())
    y = pd.DataFrame(data['label'])
    X = data.drop(['label', 'length'], axis=1)

    #X = data.loc[:, data.columns not in ['label','length']]

    feature_labels = X.columns
    print(y['label'].unique())
    X_train, X_test, y_train, y_test = train_test_split(
        np.array(X), y, test_size=0.3, random_state=42
    )
    for target in tqdm(y['label'].unique()):
        learner = CN2Unordered(max_star_size = max_star_size, 
                                max_rules = max_rules, 
                                target_class = target, 
                                evaluation_func = evaluation_func, 
                                feature_labels = feature_labels,
                                verbose = 'total')
        learner.fit(X_train, y_train)
        print(f'----- {target} -----')
        learner.print_rules()
        learner.print_conf_matrix(X_test, y_test)
        learner.print_ontology_on_file()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max_star_size', type=int, default=1)
    parser.add_argument('--max_rules', type=int, default=10)
    parser.add_argument('--evaluation_func', type=param_eval_func, default='auc_roc')
    parser.add_argument('--discr', type=param_discr, default='qcut_2', help="Parameter should be 'cut_X' o 'qcut_X'")

    args = parser.parse_args()

    start_time = time.time()
    
    gtzan_ex(args.max_star_size, args.max_rules, args.evaluation_func, args.discr)

    print("--- %s seconds ---" % (time.time() - start_time))
