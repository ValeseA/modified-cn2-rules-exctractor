from typing import Callable
import numpy as np
from sklearn.metrics import roc_auc_score

class Evaluator:
    """
    Auxiliary class created for the rules evaluation.
    Every method is implementing a metric.
    The input is always composed by:
      tp: True Positive
      tn: True Negative
      fp: False Positive
      fn: False Negative
    """
    def __init__(self, default_func: str):
        self.str_to_func = {
            'precision': self.precision,
            'recall': self.recall,
            'accuracy': self.accuracy,
            'specificity': self.specificity,
            'f1_score': self.f1_score,
            'f1_recall': self.f1_recall,
            'acc_rec': self.acc_rec,
            'acc_prec': self.acc_prec,
            'spec_rec': self.spec_rec,
            'spec_acc': self.spec_acc,
            'spec_prec': self.spec_prec,
            'spec_acc_prec_rec': self.spec_acc_prec_rec,
            'acc_prec_rec': self.acc_prec_rec,
            'auc_roc': self.auc_roc,
            'laplace_gini': self.laplace_gini,
            'laplace_precision': self.laplace_precision,
            'wracc': self.wracc,
            'gini_index': self.gini_index,
            'information_gain': self.information_gain,
            'gain_ratio': self.gain_ratio,
            'mcc': self.mcc,
            'auc_roc_sklearn': self.auc_roc_sklearn
        }
        self.default_func_name = default_func
        self.default_func = self.str_to_func.get(default_func, self.precision)

    def evaluate(self, tp: int, tn: int, fp: int, fn: int) -> float:
        return self.default_func(tp, tn, fp, fn)

    @staticmethod
    def get_menu():
        string_list = [
        'precision', 'recall', 'accuracy', 'specificity', 'f1_score', 'f1_recall', 
        'acc_rec', 'acc_prec', 'spec_rec', 'spec_acc', 'spec_prec', 'spec_acc_prec_rec',
        'acc_prec_rec', 'auc_roc', 'laplace_gini', 'laplace_precision', 'wracc', 
        'gini_index', 'information_gain', 'gain_ratio', 'mcc', 'auc_roc_sklearn'
        ]
        return string_list

    @staticmethod
    def precision(tp: int, tn: int, fp: int, fn: int) -> float:
        return tp / (tp + fp + 1e-9)

    @staticmethod
    def recall(tp: int, tn: int, fp: int, fn: int) -> float:
        return tp / (tp + fn + 1e-9)

    @staticmethod
    def accuracy(tp: int, tn: int, fp: int, fn: int) -> float:
        return (tp + tn) / (tp + tn + fp + fn)

    @staticmethod
    def specificity(tp: int, tn: int, fp: int, fn: int) -> float:
        return tn / (tn + fp + 1e-9)

    @staticmethod
    def f1_score(tp: int, tn: int, fp: int, fn: int) -> float:
        precision = Evaluator.precision(tp, tn, fp, fn)
        recall = Evaluator.recall(tp, tn, fp, fn)
        return 2 * (precision * recall) / (precision + recall + 1e-9)

    @staticmethod
    def f1_recall(tp: int, tn: int, fp: int, fn: int) -> float:
        precision = Evaluator.precision(tp, tn, fp, fn)
        recall = Evaluator.recall(tp, tn, fp, fn)
        weight_precision = 1
        weight_recall = 9
        return (weight_precision + weight_recall) / ((weight_precision / (precision + 1e-9)) + (weight_recall / (recall + 1e-9)) + 1e-9)

    @staticmethod
    def acc_rec(tp: int, tn: int, fp: int, fn: int) -> float:
        accuracy = Evaluator.accuracy(tp, tn, fp, fn)
        recall = Evaluator.recall(tp, tn, fp, fn)
        return 2 * (accuracy * recall) / (accuracy + recall + 1e-9)
    
    @staticmethod
    def acc_prec(tp: int, tn: int, fp: int, fn: int) -> float:
        accuracy = Evaluator.accuracy(tp, tn, fp, fn)
        precision = Evaluator.precision(tp, tn, fp, fn)
        return 2 * (accuracy * precision) / (accuracy + precision + 1e-9)
        
    @staticmethod
    def spec_rec(tp: int, tn: int, fp: int, fn: int) -> float:
        specificity = Evaluator.specificity(tp, tn, fp, fn)
        recall = Evaluator.recall(tp, tn, fp, fn)
        return 2 / ((1 / (specificity + 1e-9)) + (1 / (recall + 1e-9)) + 1e-9)

    @staticmethod
    def spec_acc(tp: int, tn: int, fp: int, fn: int) -> float:
        specificity = Evaluator.specificity(tp, tn, fp, fn)
        accuracy = Evaluator.accuracy(tp, tn, fp, fn)
        return 2 / ((1 / (specificity + 1e-9)) + (1 / (accuracy + 1e-9)) + 1e-9)

    @staticmethod
    def spec_prec(tp: int, tn: int, fp: int, fn: int) -> float:
        specificity = Evaluator.specificity(tp, tn, fp, fn)
        precision = Evaluator.precision(tp, tn, fp, fn)
        return 2 / ((1 / (specificity + 1e-9)) + (1 / (precision + 1e-9)) + 1e-9)

    @staticmethod
    def spec_acc_prec_rec(tp: int, tn: int, fp: int, fn: int) -> float:
        specificity = Evaluator.specificity(tp, tn, fp, fn)
        accuracy = Evaluator.accuracy(tp, tn, fp, fn)
        precision = Evaluator.precision(tp, tn, fp, fn)
        recall = Evaluator.recall(tp, tn, fp, fn)
        return 4 / ((1 / (specificity + 1e-9)) + (1 / (accuracy + 1e-9)) + (1 / (precision + 1e-9)) + (1 / (recall + 1e-9)) + 1e-9)

    @staticmethod
    def acc_prec_rec(tp: int, tn: int, fp: int, fn: int) -> float:
        accuracy = Evaluator.accuracy(tp, tn, fp, fn)
        precision = Evaluator.precision(tp, tn, fp, fn)
        recall = Evaluator.recall(tp, tn, fp, fn)

        return 3 * (accuracy * precision * recall) / (accuracy * precision + accuracy * recall + precision * accuracy + 1e-9)

    @staticmethod
    def auc_roc(tp: int, tn: int, fp: int, fn: int) -> float:
        tpr = tp / (tp + fn + 1e-9)
        fpr = fp / (fp + tn + 1e-9)
        auc_roc = (tpr + 1 - fpr) / 2
        return auc_roc

    @staticmethod
    def laplace_gini(tp: int, tn: int, fp: int, fn: int) -> float:
        return (tp + 1) / (tp + tn + 2)

    @staticmethod
    def laplace_precision(tp: int, tn: int, fp: int, fn: int) -> float:
        return (tp + 1) / (tp + fp + 2)

    @staticmethod
    def wracc(tp: int, tn: int, fp: int, fn: int) -> float:
        precision = Evaluator.precision(tp, tn, fp, fn)
        wa = precision * (tn / (tn + fn + 1e-9))
        wracc = wa / 2
        return wracc

    @staticmethod
    def gini_index(tp: int, tn: int, fp: int, fn: int) -> float:
        auc_roc = Evaluator.auc_roc(tp, tn, fp, fn)
        return 2 * auc_roc - 1

    @staticmethod
    def entropy(tp: int, tn: int, fp: int, fn: int) -> float:
        total = tp + tn + fp + fn
        p_pos = (tp + fp) / (total + 1e-9)
        p_neg = (tn + fn) / (total + 1e-9)
        if p_pos == 0 or p_neg == 0:
            return 0
        else:
            entropy_pos = -p_pos * np.log2(p_pos + 1e-9)
            entropy_neg = -p_neg * np.log2(p_neg + 1e-9)
            return entropy_pos + entropy_neg

    @staticmethod
    def information_gain(tp: int, tn: int, fp: int, fn: int) -> float:
        parent_entropy = Evaluator.entropy(tp, tn, fp, fn)
        total = tp + tn + fp + fn
        p_pos = (tp + fp) / (total + 1e-9)
        p_neg = (tn + fn) / (total + 1e-9)
        child_entropy_pos = Evaluator.entropy(tp, tn, 0, 0)
        child_entropy_neg = Evaluator.entropy(0, 0, fp, fn)
        child_entropy = p_pos * child_entropy_pos + p_neg * child_entropy_neg
        return parent_entropy - child_entropy

    @staticmethod
    def gain_ratio(tp: int, tn: int, fp: int, fn: int) -> float:
        gain = Evaluator.information_gain(tp, tn, fp, fn)
        total = tp + tn + fp + fn
        p_pos = (tp + fp) / (total + 1e-9)
        p_neg = (tn + fn) / (total + 1e-9)
        split_info = -p_pos * np.log2(p_pos + 1e-9) - p_neg * np.log2(p_neg + 1e-9)
        if split_info == 0:
            return 0
        else:
            return gain / split_info
    
    @staticmethod
    def mcc(tp: int, tn: int, fp: int, fn: int) -> float:
        numerator = (tp * tn) - (fp * fn)
        denominator = np.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
        if denominator == 0:
            mcc = 0
        else:
            mcc = numerator / denominator
        
        return mcc

    @staticmethod
    def auc_roc_sklearn(tp: int, tn: int, fp: int, fn: int) -> float:
        y_true = [1] * (tp + fn) + [0] * (tn + fp)
        y_scores = [1] * tp + [0] * fn + [1] * fp + [0] * tn
        auc_roc = roc_auc_score(y_true, y_scores)
        return auc_roc
