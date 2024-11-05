import pandas as pd
from prop import Prop, TProp
import re
from probabilities import new_prob
import os
from tqdm import tqdm

# Function to load and preprocess the dataset
def read_data():
    discretization_method = 'qcut_2'  # Discretization rule with quantile-based cut
    # Dictionary mapping number of labels to category names
    labels_dict = {
                  2: ["low", "high"],
                  3: ["low", "medium", "high"],
                  4: ["very low", "low", "high", "very high"],
                  5: ["very low", "low", "medium", "high", "very high"],
    }

    general_path = './gtzan'
    data_30 = pd.read_csv(f'{general_path}/features_30_sec.csv')  # Load 30-second features dataset
    data_3 = pd.read_csv(f'{general_path}/features_3_sec.csv')    # Load 3-second features dataset

    # Define discretization type (cut or quantile cut) and set parameters
    discretization_method = discretization_method.split('_')
    discretization = (pd.cut, 'raise', int(discretization_method[1])) if discretization_method[0] == 'cut' else (pd.qcut, 'drop', int(discretization_method[1]))
    data = data_30  # Using the 30-second dataset for processing

    # Apply discretization to all relevant columns (skip first two and last columns)
    for feature in data.columns[2:-1]:
        data[feature] = discretization[0](data[feature], discretization[2], labels=labels_dict[discretization[2]], duplicates=discretization[1])

    return data

# Convert a string representation of a TProp object to an actual TProp object
def tr_from_str(string):
    pattern = r"<T\((.*?)\) -> (.*?) : (.*?)>"
    match = re.match(pattern, string)

    if match:
        label, cond, t_val = match.groups()
        return TProp(label, cond, t_val)
    else:
        raise ValueError("Invalid string format for TProp")

# Convert a string representation of a Prop object to an actual Prop object
def r_from_str(string):
    print(string)
    pattern = r"<(.*?) -> (.*?)>"
    match = re.match(pattern, string)
    if match:
        label, cond = match.groups()
        return Prop(label, cond)
    else:
        raise ValueError("Invalid string format for Prop")

# Convert a Prop object to a lambda function representing a condition
def rule_to_lambda(prop):
    return lambda df: df[prop.var] == prop.val

# Calculate probability based on a list of TProp conditions
def get_probability(ts):
    valid, trs = zip(*ts)
    probs = [tr.t_val for tr in trs]
    print(valid)
    return new_prob(probs, valid)

# Retrieve the list of scenario files from a specified directory
def get_scenarios_list(path='scenarios/'):
    files = os.listdir(path)
    files = [f for f in files if os.path.isfile(os.path.join(path, f))]

    print(len(files))

    return files

# Process a given scenario file
def process_scenario(s_name):
    data = read_data()
    
    # Read the scenario file
    with open(f'scenarios/{s_name}', 'r') as f:
        ls = f.readlines()
    
    # Parse values for scenario, TProp and Prop conditions
    s = [float(n) for n in ls[0][1:-2].split(',')]
    trs = [tr_from_str(tr.strip()) for tr in ls[1][1:-2].split(',')]
    rs = [r_from_str(r.strip()) for r in ls[2][1:-1].split(',') if r != '']

    # Apply rigid filters based on Prop conditions
    lrs = [rule_to_lambda(r) for r in rs]
    rigid_filter = lambda df, lrs: all([lr(df) for lr in lrs])
    rigid_mask = data.apply(rigid_filter, axis=1, args=(lrs,))
    data_filtered = data[rigid_mask]
    
    # Apply filters based on TProp conditions and calculate probabilities
    trs = [tr for tr, i in zip(trs, s) if i]
    tlrs = [rule_to_lambda(r) for r in trs]
    typical_filter = lambda df, trs, tlrs: [((1, trs[i]) if tlrs[i](df) else (0, trs[i])) for i in range(len(tlrs))]         
    data_filtered['typical'] = data_filtered.apply(typical_filter, axis=1, args=(trs, tlrs))
    data_filtered['prob'] = data_filtered["typical"].apply(get_probability)

    # Save the final filtered and sorted data to a CSV file
    final = data_filtered[['filename', 'label', 'typical', 'prob']]
    final = final.sort_values(by='prob', ascending=False)
    final.to_csv(f'scenarios_csv/{s_name[:-13]}_songs.csv', index=False)

# Main entry point to process all scenarios in the specified directory
if __name__ == '__main__':
    scenarios = get_scenarios_list()
    for s in tqdm(scenarios):
        print(s)
        process_scenario(s)
