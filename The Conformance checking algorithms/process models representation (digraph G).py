#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import networkx as nx
import matplotlib.pyplot as plt

# Function to create a directed graph with sequential and contextual constraints
def create_process_model(name, sequential_constraints, contextual_constraints, bd_topics=None):
    G = nx.DiGraph()
    G.name = name
    
    # Add nodes with activity names and BD
    for activity, bd in zip(name, bd_topics):
        G.add_node(activity, BD=bd)
    
    # Add edges representing sequential and contextual constraints
    for parent, constraints in sequential_constraints.items():
        for child in constraints:
            G.add_edge(parent, child, constraint_type='sequential')
    
    for parent, constraints in contextual_constraints.items():
        for child in constraints:
            G.add_edge(parent, child, constraint_type='contextual')
    
    return G

