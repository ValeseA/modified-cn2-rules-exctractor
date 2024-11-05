import numpy as np
from Evaluator import Evaluator
from Rule import Rule
from tqdm import tqdm
import pandas as pd

from time import time



class CN2Unordered:
    """
    CN2Unordered algorithm for rule learning.
    """
    
    
    def __init__(self, 
                 max_star_size=3, 
                 max_rules=5, 
                 min_significance=0.5, 
                 target_class=None, 
                 evaluation_func = 'laplace_precision',
                 feature_labels = None,
                 feature_types = None,
                 verbose= 'no',
                 greedy_rules: bool = True):
        """
        Initialize the CN2Unordered algorithm.
        """
        self.max_star_size = max_star_size
        self.max_rules = max_rules
        self.min_significance = min_significance
        self.target_class = target_class
        self.feature_labels = feature_labels
        self.feature_types = feature_types
        self.param_verbose(verbose)
        self.verbose = verbose
        self.greedy_rules = greedy_rules
        self.rules = []
        self.param_eval_func(evaluation_func)
        self.evaluator = Evaluator(evaluation_func)
        self.generated_rules = None

    def param_eval_func(self, param):
        if param not in Evaluator.get_menu():
            raise ValueError("Parameter format is not valid")
        return param

    def param_verbose(self, param):
        if param not in ['yes','no','total']:
            raise ValueError("Parameter format is not valid")
        return param

    def fit(self, X, y):
        """
        Learn rules from the given dataset.
        """
        X, y = np.array(X), np.array(y)
        all_examples = list(zip(X, y))
        examples = list(zip(X, y))
        conflicts = set()
        
        while len(self.rules) < self.max_rules:
            all_rules = self.generate_all_rules(examples,conflicts)
            best_rule = self.find_best_rule(all_rules,examples, all_examples)

            if best_rule is None:
                break
            conf_metrics = self.calculate_conf_matrix(X,y,best_rule)
            best_rule.conf_matrix, best_rule.recall = conf_metrics[0], conf_metrics[2]

            self.rules.append(best_rule)
    
            if self.verbose == 'total':
                conflicts.update([cv for r in self.rules for cv in r.condition_values])
            else:
                examples = self.remove_covered_examples(best_rule, examples)

            if not any([True for _, y in examples if y == self.target_class]):
                if self.verbose == 'no':
                    break
                else:
                    examples = list(zip(X, y))
                    conflicts.update([cv for r in self.rules for cv in r.condition_values])

        self.generated_rules = None
        
    def generate_all_rules(self, examples, cs):
        """
        Generate all possible rules up to the maximum star size.
        """
        if not self.generated_rules:
            from itertools import combinations

            all_rules = []            
            basics_stars = set()

            basics_stars.update([(i, x[i]) for i in range(len(examples[0][0])) for x, _ in examples])
            for i in range(self.max_star_size):
                all_rules+=list(combinations(basics_stars,i+1))

            self.generated_rules = all_rules

        def conflicts(r,cs):
            l = [i for i,_ in r]
            s = set(l)
            return len(l) != len(s) or any([x in cs for x in r]) #or any([x not in values for x in l]))

        all_rules = [r for r in self.generated_rules if not conflicts(r,cs)]

        return all_rules
    
    def find_best_rule(self,rules,examples, all_examples):
        best_rule = None
        slice = 1 if self.greedy_rules else -1
        for r in tqdm(rules[::slice]):
            conditions, values = [],[]
            for i,value in r:
                conditions.append(lambda x, i=i, val=value: x[i] == val)
                values.append((i, value))
            rule = Rule(conditions, self.target_class, values, self.feature_labels, self.feature_types)
            s = self.calculate_significance(rule,examples)
            if best_rule is None or s > best_rule.significance or (s == best_rule.significance and 
            self.calculate_significance(rule,all_examples) > self.calculate_significance(best_rule,all_examples)):
                rule.significance = s
                best_rule = rule
                
        return best_rule

    def initialize_stars(self, examples):
        """
        Initialize the stars by creating rules with single conditions.
        """
        stars = []
        for i in range(len(examples[0][0])):
            values = set(x[i] for x, _ in examples)
            for value in values:
                condition = lambda x, i=i, val=value: x[i] == val
                rule = Rule([condition], self.target_class, [(i, value)], self.feature_labels, self.feature_types)
                stars.append(rule)

        return stars

    def refine_star(self, star, examples):
        """
        Refine the given star by adding conditions.
        """
        new_stars = []
        for i in range(len(examples[0][0])):
            values = set(x[i] for x, _ in examples)
            for value in values:
                condition = lambda x, i=i, val=value: x[i] == val
                if (i, value) not in star.condition_values:
                    new_star_conditions = star.conditions + [condition]
                    new_star_values = star.condition_values + [(i, value)]
                    new_star = Rule(new_star_conditions, self.target_class, new_star_values, self.feature_labels)
                    new_stars.append(new_star)

        return new_stars

    def prediction_single_rule(self, rule, examples):
        tp, tn, fp, fn = 0, 0, 0, 0
        for x, y in examples:
            if rule.matches(x):
                if y == rule.prediction:
                    tp += 1
                else:
                    fp += 1
            else:
                if y == rule.prediction:
                    fn += 1
                else:
                    tn += 1
            
        return tp,tn,fp,fn

    def calculate_significance(self, rule, examples):
        """
        Calculate the significance of the given rule.
        """
        tp, tn, fp, fn = self.prediction_single_rule(rule,examples)

        significance = self.evaluator.evaluate(tp, tn, fp, fn)
        
        return significance

    def remove_covered_examples(self, rule, examples):
        """
        Remove the examples covered by the given rule.
        """
        return [(x, y) for x, y in examples if not rule.matches(x) or y != self.target_class]

    def predict(self, X, input_rule):
        """
        Predict the class labels for the given examples.
        """
        X = np.array(X)
        predictions = []
        if input_rule is None:
            for x in X:
                match = False
                for rule in self.rules:
                    if rule.matches(x):
                        predictions.append(rule.prediction)
                        match = True
                        break

                if not match:
                    predictions.append(None)
        else:
            for x in X:
                if input_rule.matches(x):
                    predictions.append(input_rule.prediction)
                else:
                    predictions.append(None)
        return predictions

    def calculate_conf_matrix(self, X, ys, input_rule=None):
        """
        Calculate confusion matrix and some metrics on a given X and y
        """
        X = np.array(X)
        ys = np.array(ys)
        
        tp, tn, fp, fn = 0, 0, 0, 0
        predictions = self.predict(X,input_rule)

        for pred, true in zip(predictions,ys):
            if pred == self.target_class:
                if pred == true:
                    tp += 1
                else:
                    fp += 1
            else:
                if true == self.target_class:
                    fn += 1
                else:
                    tn += 1

        precision = tp / (tp + fp + 1e-9)

        recall = 0
        if tp + fn > 0 :
            recall = tp / (tp + fn)

        accuracy = (tp + tn) / len(ys)

        specificity = tn / (tn + fp + 1e-9)

        f1_score = 2 * (precision * recall) / (precision + recall + 1e-9)

        tpr = tp / (tp + fn + 1e-9)
        fpr = fp / (fp + tn + 1e-9)
        auc_roc = (tpr + 1 - fpr) / 2

        # first is confusion matrix
        return [[tp, fp], [fn, tn]], precision, recall, accuracy, specificity, f1_score, auc_roc

    def print_conf_matrix(self, X, y):
        """
        Print confusion matrix and some metrics on a given X and y calling print_conf_matrix().
        """
        conf_matrix, prec, rec, acc, spec, f1, auc_roc = self.calculate_conf_matrix(X,y)
        
        print('Confusion Matrix:\n', conf_matrix)
        print('Precision: ',prec)
        print('Recall: ', rec)
        print('Accuracy: ', acc)
        print('Specificity: ', spec)
        print('F1 Score: ', f1)
        print('AUC-ROC: ', auc_roc)

    def print_rules(self):
        """
        Print the rules in a human-readable format.
        """
        for i, rule in enumerate(self.rules):

            print(f"Rule {i + 1}: {rule}")

    def print_ontology_on_file(self):
        for i, rule in enumerate(self.rules):
            print(f"Rule {i + 1}: {rule.print_ontology()}")

    def to_excel(self, file_name, sheet_name='Sheet1'):

        from math import sqrt
        import os

        if not os.path.isfile(f'{file_name}.xlsx'):
            writer = pd.ExcelWriter(f'{file_name}.xlsx', engine='openpyxl', mode='w')
        else:
            writer = pd.ExcelWriter(f'{file_name}.xlsx', engine='openpyxl', mode='a',if_sheet_exists='overlay')

        x = int(sqrt(len(self.rules))) if int(sqrt(len(self.rules))) < 10 else 10
        coord = [(i%x*5+2,i//x*5) for i in range(len(self.rules))]
        
        # Create dataframes for each confusion matrix
        for i, rule in enumerate(self.rules):
            df = pd.DataFrame(rule.conf_matrix, columns=['Real True','Real False'], index=['Pred True','Pred False'])
            df.to_excel(writer, sheet_name=sheet_name, startrow=coord[i][0], startcol=coord[i][1])
            writer.sheets[sheet_name].cell(coord[i][0]+1,coord[i][1]+1).value = f"Rule {i + 1}: {rule}"
        
        writer.sheets[sheet_name].cell(1,1).value = (f'Description: max_star_size={self.max_star_size}, max_rules={self.max_rules},'+
                                                    f'min_significance={self.min_significance},target_class={self.target_class},'+ 
                                                    f'evaluation_func={self.evaluator.default_func_name},'+
                                                    f'verbose={self.verbose}, greedy_rules={self.greedy_rules}')
        writer.close()
