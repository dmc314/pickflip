import os
import numpy as np
# import pandas as pd
import text_similarity
import text_pipeline

from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource

# Set up Flask App
top_tags_api = Flask(__name__)
api = Api(top_tags_api)  


class GetTopTags(Resource):
    @staticmethod
    def post():

        # Validate the request body contains JSON
        if request.is_json:

            # Parse the JSON into a Python dictionary
            req = request.get_json()
    
            # Expecting these arguments from request JSON as comma separated list of model inputs...
            list_of_query_texts = req.get("list_of_query_texts")
            list_of_candidate_tag_texts = req.get("list_of_candidate_tag_texts")
            if "top_k_predictions" in req:
                top_k = int(req.get("top_k_predictions"))
            else:
                top_k = 1
            if "min_prob_score" in req:
                threshold = float(req.get("min_prob_score"))
            else:
                threshold = 0.01    

            # Clean and preprocess text 
            processed_queries = [text_pipeline.text_preprocess(text) for text in list_of_query_texts]
            processed_cands = [text_pipeline.text_preprocess(text) for text in list_of_candidate_tag_texts]

            # Run model to make inference/prediction
            dict_of_outputs = categorize.find_top_tags(processed_queries, processed_cands, top_k, threshold)

            response_body = {
                "top_tags": dict_of_outputs,
            }
        
            res = make_response(jsonify(response_body), 200)
            return res
    
        else:

            # The request body wasn't JSON so return a 400 HTTP status code
            return make_response(jsonify({"message": "Request body must be JSON"}), 400)


class GetVectors(Resource):
    @staticmethod
    def post():

        # Validate the request body contains JSON
        if request.is_json:

            # Parse the JSON into a Python dictionary
            req = request.get_json()
    
            # Expecting these arguments from request JSON as comma separated list of model inputs...
            list_of_texts = req.get("list_of_texts")

            # Clean and preprocess text 
            processed_texts = [text_pipeline.text_preprocess(text) for text in list_of_texts]
            
            # Run model to make inference/prediction
            list_of_outputs = categorize.get_vectors(processed_texts)

            response_body = {
                "vector_list": str(list_of_outputs),
            }
        
            res = make_response(jsonify(response_body), 200)
            return res
    
        else:

            # The request body wasn't JSON so return a 400 HTTP status code
            return make_response(jsonify({"message": "Request body must be JSON"}), 400)


api.add_resource(GetTopTags, '/get_tag_recs_from_list')
api.add_resource(GetVectors, '/get_vectors')
if __name__ == '__main__':
   top_tags_api.run(host="0.0.0.0", port=1999, debug=False)
