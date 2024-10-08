import pandas as pd
import json

def generate_combinations(lists):
    combinations = [[]]
    
    for sublist in lists:
        new_combinations = []
        
        for combination in combinations:
            for item in sublist:
                new_combinations.append(combination + [item])
        
        combinations = new_combinations
    
    return combinations


file_path = '/Users/satviksawhney/Downloads/ML_CLASS/Cabelteque/CDL Virus Assignment (Y V0).xlsx'
excel_data = pd.ExcelFile(file_path)


signature_df = pd.read_excel(excel_data, sheet_name='signature ')


general_df = pd.read_excel(excel_data, sheet_name='general')
general_data = {}
for col in general_df.columns:
    general_data[col] = general_df.at[0, col]


dependent_data = {}
for sheet_name in excel_data.sheet_names:
    if sheet_name not in ['signature ', 'general']:
        dependent_data[sheet_name] = pd.read_excel(excel_data, sheet_name=sheet_name)

designators = signature_df.columns.tolist()

designator_values = []

for designator in designators:
    values = signature_df[designator].dropna().tolist()
    designator_values.append(values)
    
all_combinations = generate_combinations(designator_values)

virus_mutations = []
for combination in all_combinations:
    mutation = {"signature ": ''.join(map(str, combination))}
    mutation.update(general_data)
    
    for sheet_name, df in dependent_data.items():
        for index, row in df.iterrows():
            designator_value = row[df.columns[0]]
            if designator_value in combination:
                mutation.update(row[1:].dropna().to_dict())
    
    virus_mutations.append(mutation)

json_output = json.dumps(virus_mutations, indent=4)
with open('/Users/satviksawhney/Downloads/ML_CLASS/Cabelteque/virus_mutations_0.json', 'w') as json_file:
    json_file.write(json_output)
