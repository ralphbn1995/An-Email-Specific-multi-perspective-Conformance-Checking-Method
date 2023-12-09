#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from collections import Counter
from itertools import combinations

def calculate_coexistence_counts(activities, associations):
    # Calculate the coexistence counts of BD with each pair of sequential activities
    coexistence_counts = {activity_pair: Counter() for activity_pair in combinations(activities, 2)}
    for thread in associations:
        for activity, bds in thread.items():
            if activity in activities:
                for other_activity in activities:
                    if other_activity != activity:
                        activity_pair = tuple(sorted([activity, other_activity]))
                        coexistence_counts[activity_pair].update(bds)
    
    return coexistence_counts

def generate_constraints(activities, c1, c2):
    # Combine the two lists of sequential constraints
    sequential_constraints = c1 + c2
    
    # Extract all unique threads from the sequential constraints
    threads = [{activity: bds for activity, bds in constraint.items() if activity in activities} for constraint in sequential_constraints]
    
    # Calculate the coexistence counts for each pair of sequential activities
    coexistence_counts = calculate_coexistence_counts(activities, threads)
    
    constraints = []
    for activity_pair, count in coexistence_counts.items():
        most_frequent_bd = count.most_common(1)[0][0]
        constraint = f"{activity_pair[0]} -> {activity_pair[1]} => {most_frequent_bd}"
        constraints.append(constraint)
    
    return constraints


# In[ ]:




