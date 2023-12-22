#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from transformers import BertTokenizer, BertModel
import umap
import hdbscan
import numpy as np

# Load the BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

# Function to convert BD into BERT embeddings
def get_bert_embeddings(texts):
    input_ids = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")["input_ids"]
    with torch.no_grad():
        outputs = model(input_ids)
    embeddings = outputs.last_hidden_state.mean(dim=1).numpy()
    return embeddings

# Function to perform topic modeling
def topic_modeling(BD, num_topics):
    # Get BERT embeddings for the BD
    embeddings = get_bert_embeddings(BD)

    # Perform dimensionality reduction with UMAP
    reducer = umap.UMAP(n_components=2, random_state=42)
    reduced_embeddings = reducer.fit_transform(embeddings)

    # Perform clustering with HDBSCAN
    clusterer = hdbscan.HDBSCAN(min_cluster_size=5, min_samples=1, allow_single_cluster=False)
    cluster_labels = clusterer.fit_predict(reduced_embeddings)

    # Create DataFrame to store results
    topic_model_df = pd.DataFrame({"BD": BD, "Cluster": cluster_labels})

    # Identify exemplars for each cluster (representative BD)
    topic_exemplars = topic_model_df.groupby("Cluster").apply(lambda group: group.iloc[0]).reset_index(drop=True)

    return topic_exemplars

