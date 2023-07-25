#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from collections import Counter
from itertools import combinations

def calculate_coexistence_coefficient(activities, associations):
    # Calculate the coexistence of BD with each activity
    coexistence_counts = {activity: Counter() for activity in activities}
    for thread in associations:
        for activity, bds in thread.items():
            for bd in bds:
                coexistence_counts[activity][bd] += 1
    
    # Calculate the most frequently associated BD for each activity
    most_frequent_bd = {activity: count.most_common(1)[0][0] for activity, count in coexistence_counts.items()}
    
    # Calculate the coexistence coefficient for each BD
    coexistence_coefficients = {}
    for bd in set(bd for bds in associations for bd in bds):
        bd_coexistence = sum(1 for activity in activities if most_frequent_bd[activity] == bd)
        coexistence_coefficients[bd] = bd_coexistence / len(activities)
    
    return most_frequent_bd, coexistence_coefficients

def generate_constraints(activities, associations, coefficient_threshold):
    constraints = []
    most_frequent_bd, coexistence_coefficients = calculate_coexistence_coefficient(activities, associations)
    
    for activity in activities:
        associated_bds = [bd for bd, coefficient in coexistence_coefficients.items() if coefficient > coefficient_threshold and most_frequent_bd[activity] == bd]
        if associated_bds:
            constraint = f"{activity} => {','.join(associated_bds)}"
            constraints.append(constraint)
    
    return constraints

