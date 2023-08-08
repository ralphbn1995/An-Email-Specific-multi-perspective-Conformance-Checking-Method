def retrieveBD(activity):
    # Function to retrieve BD based on activity
    pass

def calculate_coexistence_rate(activity, bd):
    # Function to calculate coexistence rate
    pass

def generate_constraints(activity, bd):
    return f"{activity} ALWAYSWITH {bd}"

def extract_relations(log):
    frequency_dict = {}
    for event in log:
        activity = event["activity"]
        bd = retrieveBD(activity)
        
        if activity not in frequency_dict:
            frequency_dict[activity] = {}
        
        for bd_element in bd:
            if bd_element not in frequency_dict[activity]:
                frequency_dict[activity][bd_element] = 0
            frequency_dict[activity][bd_element] += 1
    
    threshold = 0.5
    high_occ_list = []
    for activity, bd_elements in frequency_dict.items():
        for bd_element, count in bd_elements.items():
            coexistence_rate = calculate_coexistence_rate(activity, bd_element)
            if coexistence_rate > threshold:
                high_occ_list.append((activity, bd_element))
    
    relation_constraints = []
    for activity, bd_element in high_occ_list:
        constraint = generate_constraints(activity, bd_element)
        relation_constraints.append(constraint)
    
    return relation_constraints

# Example log format: [{"activity": "activity_1"}, {"activity": "activity_2"}, ...]
example_log = [
    {"activity": "activity_1"},
    {"activity": "activity_1"},
    {"activity": "activity_2"},
    {"activity": "activity_2"},
    # ...
]

relation_constraints = extract_relations(example_log)
for constraint in relation_constraints:
    print(constraint)
