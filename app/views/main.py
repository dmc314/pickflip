from flask import Flask, jsonify, request, make_response, render_template
from app import app
import random
import text_similarity
import text_pipeline


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/map')
def map():
    return render_template('map.html', title='Map')


@app.route('/map/refresh', methods=['POST'])
def map_refresh():
    points = [(random.uniform(48.8434100, 48.8634100),
               random.uniform(2.3388000, 2.3588000))
              for _ in range(random.randint(2, 9))]
    return jsonify({'points': points})


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


# DAVE added route for similarity prediction

@app.route('/predict_sim.html', methods=["POST", "GET"])
def predict_sim():

    if len(request.form['query_texts']) > 0:
        query_texts = request.form['query_texts']
    else:
        query_texts = ['i like chicken', 'human resources mgmt']
    if len(request.form['candidate_texts']) > 0:
        candidate_texts = request.form['candidate_texts']
    else:
        candidate_texts = ['i love chicken', 'employment management']
    if len(request.form['top_k']) > 0:
        top_k = request.form['top_k']
    else:
        top_k = 3
    threshold = 0

    # Clean and preprocess text 
    processed_queries = [text_pipeline.text_preprocess(text) for text in query_texts]
    processed_cands = [text_pipeline.text_preprocess(text) for text in candidate_texts]

    # Run model to make inference/prediction
    dict_of_outputs = text_similarity.find_top_tags(processed_queries, processed_cands, top_k, threshold)

    return jsonify(dict_of_outputs)
    # return render_template('predict_sim.html', tables=[df_users.to_html(classes='data')], titles=df_users.columns.values)
    # return render_template('predict_sim.html', header='Similarity Results', content=str(jsonify(dict_of_outputs)))
