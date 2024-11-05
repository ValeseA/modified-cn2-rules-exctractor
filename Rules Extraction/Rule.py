class Rule:
    """
    Rule class representing a rule in CN2Unordered algorithm.
    """

    def __init__(self, conditions, prediction, condition_values, feature_labels = None, feature_types = None):
        """
        Initialize the Rule object.
        """
        self.conditions = conditions
        self.prediction = prediction
        self.condition_values = condition_values
        self.feature_labels = feature_labels
        self.feature_types = feature_types
        self.significance = None
        self.conf_matrix = []
        self.recall = None

    def matches(self, x):
        """
        Check if the rule matches the given example.
        """
        return all(condition(x) for condition in self.conditions)

    def __str__(self):
        if self.feature_labels is None:
            conditions_str = " AND ".join(f"x[{i}] == {value}" for i, value in self.condition_values)
        else:
            conditions_str = " AND ".join(f"{self.feature_labels[i]} == {value}" for i, value in self.condition_values)

        return f"IF {conditions_str} THEN y == {self.prediction} : {self.conf_matrix} : {self.significance}"

    def print_ontology(self):
        if self.feature_labels is None:
            conditions_str = " AND ".join(f"x[{i}] == {value}" if (not self.feature_types or self.feature_types[i] != bool) else f"{'not ' if int(value) == 0  else ''}x[{i}]" for i, value in enumerate(self.condition_values))
        else:
            conditions_str = " AND ".join(f"{self.feature_labels[i]} == {value}" if (not self.feature_types or self.feature_types[i] != bool) else f"{'not ' if int(value) == 0 else ''}{self.feature_labels[i]}" for i, value in self.condition_values)

        if self.recall == 1:
            class_str = f"{self.prediction}"
            recall_str = ""
        else:
            class_str = f"T({self.prediction})"
            recall_str = f" :  {round(self.recall,3)}"

        return f"{class_str} -> {conditions_str}{recall_str}"
