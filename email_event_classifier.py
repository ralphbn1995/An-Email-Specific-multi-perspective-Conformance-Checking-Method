import numpy as np
from scipy.spatial.distance import cosine

class EventClassifier:
    def __init__(self, email_process_model, threshold):
        self.email_process_model = email_process_model
        self.threshold = threshold

    def match(self, event, activity):
        matching_nodes = [node for node in self.email_process_model.get_child_nodes(event) if self.email_process_model.get_activity(node) == activity]
        return any(matching_nodes)

    def similarity(self, node, emb_bd):
        emb_node = self.email_process_model.get_embedding(node)
        return 1 - cosine(emb_node, emb_bd)

    def classify_event(self, event):
        current_node = self.email_process_model.get_starting_node()
        emb_bd = self.email_process_model.get_embedding_for_bd(event.bd)

        while current_node is not None:
            if self.match(event, self.email_process_model.get_activity(current_node)):
                sim_score = self.similarity(current_node, emb_bd)
                if sim_score > self.threshold:
                    return "Fulfilling"
                else:
                    return "Violating"
            current_node = self.email_process_model.get_next_node(current_node)
        
        return "Violating"

    def revise_expected_pathway(self, event):
        current_node = self.email_process_model.get_starting_node()
        next_node = None

        while current_node is not None:
            if self.match(event, self.email_process_model.get_activity(current_node)):
                next_nodes = [node for node in self.email_process_model.get_child_nodes(current_node) if self.match(event, self.email_process_model.get_activity(node))]
                if next_nodes:
                    next_node = next_nodes[0]
                break
            current_node = self.email_process_model.get_next_node(current_node)
        
        if next_node is not None:
            return next_node
        else:
            return current_node

class EmailProcessModel:
    def __init__(self, graph, embeddings):
        self.graph = graph
        self.embeddings = embeddings

    def get_child_nodes(self, node):
        return self.graph[node]

    def get_activity(self, node):
        return self.graph[node]['activity']

    def get_embedding(self, node):
        return self.embeddings[node]

    def get_embedding_for_bd(self, bd):
        # Calculate the average embedding of the values in bd using topic modeling
        avg_embedding = np.mean([self.embeddings[value] for value in bd], axis=0)
        return avg_embedding

    def get_starting_node(self):
        # Return the root node or starting node of the process
        return 'root'

    def get_next_node(self, node):
        # Return the next node based on the graph transitions
        if 'next' in self.graph[node]:
            return self.graph[node]['next']
        else:
            return None

# Example usage
graph = {
    'root': {'activity': 'Start', 'next': 'node1'},
    'node1': {'activity': 'Task1', 'next': 'node2'},
    'node2': {'activity': 'Task2', 'next': 'node3'},
    'node3': {'activity': 'End'}
}

embeddings = {
    'Start': np.array([0.2, 0.3, 0.4]),
    'Task1': np.array([0.5, 0.6, 0.7]),
    'Task2': np.array([0.8, 0.9, 1.0]),
    'End': np.array([1.1, 1.2, 1.3])
}

email_process_model = EmailProcessModel(graph, embeddings)
threshold = 0.8
classifier = EventClassifier(email_process_model, threshold)

class Event:
    def __init__(self, activity, bd):
        self.activity = activity
        self.bd = bd

event = Event('Task1', ['value1', 'value2'])
classification = classifier.classify_event(event)
print("Classification:", classification)

next_node = classifier.revise_expected_pathway(event)
print("Next Node:", next_node)
