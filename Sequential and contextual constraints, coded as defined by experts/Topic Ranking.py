#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np

def calculate_similarity(embeddings):
    """
    Calculate the similarity matrix between topics based on their embeddings.

    Parameters:
        embeddings (dict): A dictionary representing the embeddings of topics. The keys should be topic nodes,
                           and the values should be the corresponding embeddings.

    Returns:
        dict: A similarity matrix where keys are topic nodes, and values are dictionaries mapping other topic
              nodes to their corresponding similarity scores.
    """

    # Replace this with the actual similarity calculation method based on embeddings
    # For illustration, we'll use a random similarity matrix here
    similarity_matrix = {}
    for topic in embeddings:
        similarity_matrix[topic] = {other_topic: np.random.rand() for other_topic in embeddings if other_topic != topic}

    return similarity_matrix


def create_graph(similarity_matrix, threshold):
    """
    Create a graph representing relationships between topics based on a similarity matrix.

    Parameters:
        similarity_matrix (dict): A dictionary representing the similarity between topics. The keys should be
                                  topic nodes, and the values should be dictionaries mapping other topic nodes
                                  to their corresponding similarity scores.
        threshold (float): The threshold for establishing connections between topics. If the similarity score
                           between two topics is greater than or equal to the threshold, they will be connected.

    Returns:
        dict: A dictionary representing the graph. The keys are topic nodes, and the values are lists of topic
              nodes that link to the corresponding key.
    """

    graph = {}

    # Iterate through each topic node in the similarity matrix
    for node in similarity_matrix:
        graph[node] = []

        # Find topics with similarity greater than or equal to the threshold and connect them
        for other_node, similarity_score in similarity_matrix[node].items():
            if similarity_score >= threshold:
                graph[node].append(other_node)

    return graph


def pagerank(graph, d=0.85, max_iter=100, tol=1e-6):
    """
    Calculate the PageRank scores for nodes in the graph.

    Parameters:
        graph (dict): The graph representing relationships between topics. It should be a dictionary where
                      keys are topic nodes and values are lists of topic nodes that link to the corresponding key.
        d (float): The damping factor, representing the probability of jumping to a random topic (default is 0.85).
        max_iter (int): The maximum number of iterations for convergence (default is 100).
        tol (float): The tolerance for convergence (default is 1e-6).

    Returns:
        dict: A dictionary containing the topic nodes as keys and their corresponding PageRank scores as values.
    """

    # Get the total number of topics
    N = len(graph)

    # Initialize the probability scores for each topic node
    pr_scores = {node: 1 / N for node in graph}

    for _ in range(max_iter):
        new_pr_scores = {}
        diff = 0

        # Calculate the new probability scores for each topic node
        for node in graph:
            incoming_topics = [n for n in graph if node in graph[n]]
            incoming_score = sum(pr_scores[incoming_topic] / len(graph[incoming_topic]) for incoming_topic in incoming_topics)

            new_pr_score = (1 - d) / N + d * incoming_score
            new_pr_scores[node] = new_pr_score

            # Calculate the difference in probability scores for convergence check
            diff += abs(new_pr_score - pr_scores[node])

        # Check for convergence
        if diff < tol:
            break

        pr_scores = new_pr_scores

    return pr_scores

