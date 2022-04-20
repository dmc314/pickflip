# import pandas as pd
import numpy as np
# import re, csv
# from datetime import datetime
import scipy
from scipy import spatial
from app.toolbox import text_pipeline

from sentence_transformers import SentenceTransformer
ft_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load FastText model
# ft_model_filename = "models/fasttext_categorizer_2022-01-01.bin"
# ft_model = fasttext.load_model(ft_model_filename)


def get_vectors(list_of_texts):
# Return list of vector embeddings from list of texts
    list_of_vectors = [ft_model.encode(text) for text in list_of_texts]
    return list_of_vectors


def cosine_similarity(vector1, vector2):
    return 1 - scipy.spatial.distance.cosine(vector1,vector2)


def find_top_tags(list_of_query_texts, list_of_candidate_tags, top_k, threshold):

    query_vectors = get_vectors(list_of_query_texts)
    candidate_vectors = get_vectors(list_of_candidate_tags)
    tag_results = {}
    list_of_top_tags = []
    
    for i, query_vector in enumerate(query_vectors):
        tag_results[i] = {}
        tag_results[i]['query_text'] = list_of_query_texts[i]
        
        unranked_cand_scores = []
        for j, candidate_vector in enumerate(candidate_vectors):

            # Score vector embeddings on cosine similarity
            unranked_cand_scores.append(cosine_similarity(query_vector,candidate_vector))

            ranked_top_k_indexes = sorted(range(len(unranked_cand_scores)), \
                    key=lambda i: unranked_cand_scores[i], reverse=True)[:top_k]
            tag_results[i]['probas']  = [unranked_cand_scores[i] for \
                    i in ranked_top_k_indexes if unranked_cand_scores[i]>threshold]
            tag_results[i]['predictions'] = [list_of_candidate_tags[i] for \
                    i in ranked_top_k_indexes if unranked_cand_scores[i]>threshold]

        list_of_top_tags.append(list_of_candidate_tags[ranked_top_k_indexes[0]])

    return tag_results #, list_of_top_tags

