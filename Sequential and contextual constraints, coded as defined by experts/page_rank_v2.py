import numpy as np

def pagerank(graph, damping_factor=0.85, convergence_threshold=1e-6, max_iterations=100):
    """
    Calculate PageRank scores for nodes in a directed graph.

    Parameters:
    - graph: The directed graph represented as an adjacency matrix (numpy array).
    - damping_factor: The probability of following a link (usually set to 0.85).
    - convergence_threshold: The threshold for convergence (stop iterating if the change in scores is below this).
    - max_iterations: Maximum number of iterations.

    Returns:
    - A dictionary where keys are node indices and values are their corresponding PageRank scores.
    """
    num_nodes = len(graph)
    initial_score = 1 / num_nodes
    scores = np.full(num_nodes, initial_score)  # Initialize scores

    for _ in range(max_iterations):
        prev_scores = scores.copy()

        for i in range(num_nodes):
            incoming_nodes = np.where(graph[:, i] > 0)[0]
            score_sum = np.sum(prev_scores[incoming_nodes] / np.sum(graph[incoming_nodes, :], axis=1))
            scores[i] = (1 - damping_factor) / num_nodes + damping_factor * score_sum

        # Check for convergence
        if np.linalg.norm(scores - prev_scores, 1) < convergence_threshold:
            break

    result = {i: score for i, score in enumerate(scores)}
    return result

# Example usage
if __name__ == "__main__":
    # Example directed graph represented as an adjacency matrix
    adjacency_matrix = np.array([
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 1, 0, 0],
        [0, 0, 1, 0]
    ], dtype=float)

    # Run PageRank algorithm
    result = pagerank(adjacency_matrix)

    # Print the PageRank scores
    for node, score in result.items():
        print(f"Node {node}: PageRank Score = {score:.4f}")
