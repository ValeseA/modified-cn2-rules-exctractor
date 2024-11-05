import pandas as pd
import os
import json
from tqdm import tqdm

# Function to parse a scenario
def parse_scenario(s):
    '''
    Example Input:
    s = [
        [0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 9.075],
        [
            <T(blues) -> mfcc9_mean == low : 0.8>,
            <T(blues) -> spectral_centroid_mean == low : 0.874>,
            ...
        ],
        []
    ]
    '''
    is_valid, t_rules, r_rules = s
    t_rules = t_rules[1:-1].split(', ')  # Parse typical rules
    is_valid = is_valid[1:-1].split(', ')

    tipical = str(list(zip(is_valid[:-1], t_rules))).replace("'", "")
    t_parsed = parse_typical(tipical)
    
    r_rules = r_rules[1:-1]
    r_parsed = []

    if r_rules:
        r_rules = r_rules.split(', ')
        r_parsed = []
        for rule in r_rules:
            rule = rule[1:-1]

            label = rule.split(' -> ')[0]
            prop = rule.split(' -> ')[1].split(' == ')[0]
            val = rule.split(' == ')[1]
            r_parsed.append({'label': label,
                             'prop': prop,
                             'val': val})

    result = {'scenario_label': '', 'rigid': r_parsed, 'typical': t_parsed}
    return result 

# Function to parse typical rules from a string format
def parse_typical(tipical_str):
    '''
    Example Input:
    [(1, <T(blues) -> mfcc9_mean == low : 0.8>), (1, <T(blues) -> spectral_centroid_mean == low : 0.794>), ...]
    '''
    typical_strs = tipical_str[1:-1].split(',')

    typical_strs = [f"{num.strip()[1:]};{char.strip()[:-1]}" for num, char in zip(typical_strs[::2], typical_strs[1::2])]
    
    result = []
    for tstr in typical_strs:
        is_true, rule = tstr.split(';')
        label = rule.split('(')[1].split(')')[0]
        prop = rule.split(' -> ')[1].split(' == ')[0]
        val = rule.split(' == ')[1].split(' : ')[0]
        prob = rule.split(' : ')[1][:-1]
        result.append({'is_true': is_true,
                       'label': label,
                       'prop': prop,
                       'val': val,
                       'prob': prob})
    return result

# Function to get a list of scenario files in the CSV path
def get_scenarios_list(csv_path='scenarios_csv/'):
    csv_files = os.listdir(csv_path)
    csv_files = [f for f in csv_files if os.path.isfile(os.path.join(csv_path, f))]
    return csv_files

scenarios = get_scenarios_list()

# Process each scenario file and parse it
for s in tqdm(scenarios):
    df = pd.read_csv(f'scenarios_csv/{s}')
    n = '_'.join(s.split('_')[:-1])

    scenario_name = f'{n}_scenario.txt'
    with open(f'scenarios/{scenario_name}', 'r') as sn:
        s_file = sn.readlines()

    final_dict = parse_scenario(s_file)
    final_dict['scenario_label'] = n
    
    # Filter the dataframe by probability threshold
    df = df[df['prob'] >= 0.9]

    # Parse and add typical information to the dataframe
    df['typical_parsed'] = df['typical'].apply(parse_typical)

    df = df.drop(columns=['typical'])  # Drop original typical column

    final_dict['songs_list'] = df.to_dict(orient='records')  # Add song list data to result

    # Write the parsed data to a JSON file
    json_result = json.dumps(final_dict, indent=4)
    with open(f'scenarios_json/{n}.json', 'w') as file:
        file.write(json_result)
