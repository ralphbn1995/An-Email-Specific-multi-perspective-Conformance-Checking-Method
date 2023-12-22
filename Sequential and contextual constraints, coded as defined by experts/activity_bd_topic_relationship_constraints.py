from transformers import BertModel, BertTokenizer
import umap
import hdbscan
import networkx as nx
import numpy as np
from scipy.spatial.distance import cosine
from sklearn.feature_extraction.text import CountVectorizer
from pagerank import pagerank  # Assuming you have a pagerank module

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = BertModel.from_pretrained('bert-base-uncased')

def BERT_encode(text):
    # Encode text using BERT
    tokens = tokenizer.encode(text, add_special_tokens=True)
    inputs = tokenizer.batch_encode_plus([tokens], return_tensors='pt', pad_to_max_length=True)
    outputs = bert_model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
    return embeddings

def UMAP_reduce(embeddings):
    # Reduce dimensionality using UMAP
    reducer = umap.UMAP()
    reduced_embeddings = reducer.fit_transform(embeddings)
    return reduced_embeddings

def HDBSCAN_cluster(reduced_embeddings):
    # Cluster using HDBSCAN
    clusterer = hdbscan.HDBSCAN(min_cluster_size=5, metric='euclidean')
    clusters = clusterer.fit_predict(reduced_embeddings)
    return clusters

def calculate_cluster_center(cluster_indices, dataset):
    # Calculate the center of the cluster
    cluster_points = dataset[cluster_indices]
    cluster_center = np.mean(cluster_points, axis=0)
    return cluster_center

def find_closest_point(cluster_center, cluster_indices, dataset):
    # Find the index of the closest point to the cluster center
    distances = [np.linalg.norm(cluster_center - dataset[i]) for i in cluster_indices]
    closest_point_idx = cluster_indices[np.argmin(distances)]
    return closest_point_idx

def analyze_and_label(exemplar):
    # Analyze the exemplar to generate a topic label
    # Replace this with your actual analysis
    return f"Topic_{np.random.randint(1, 10)}"

def rank_topics(graph):
    # Rank topics using PageRank algorithm
    return pagerank(graph)

def identify_related_topics(bd_set):
    # Identify related topics using the topic model
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(bd_set)
    terms = vectorizer.get_feature_names_out()

    # Build a graph to represent relationships between topics
    graph = nx.DiGraph()

    for i in range(len(bd_set) - 1):
        for j in range(i + 1, len(bd_set)):
            similarity = 1 - cosine(X[i].toarray(), X[j].toarray())
            if similarity > 0.5:  # Adjust the threshold as needed
                topic_i = analyze_and_label(bd_set[i])
                topic_j = analyze_and_label(bd_set[j])
                graph.add_edge(topic_i, topic_j, weight=similarity)

    return graph

def store_constraint(constraint):
    # Store constraints (replace with your actual storage implementation)
    print(f"Storing constraint: {constraint}")

def generate_constraints(thread_data):
    for thread in thread_data:
        for activity, bd_set in thread:
            # Identify related BD topics using the topic model
            related_topics = identify_related_topics(bd_set)
            
            # Rank the identified topics
            ranked_topics = rank_topics(related_topics)
            
            # Concatenate the activity name with the most significant BD topic
            constraint = f"{activity}ALWAYSWITH{list(ranked_topics.keys())[0]}"
            
            # Store the constraint
            store_constraint(constraint)

# Example usage
generate_constraints(thread_data)
