from flask import Flask, jsonify, request, make_response, render_template
from app import app
import random
from app.toolbox import text_similarity, text_pipeline
from app.toolbox import attribution_calcs

@app.route('/')
@app.route('/index')
def index():
    
    # Abeer: Figure out how to dynamically provide "current_survey" based on recommender algo
    #current_survey = get_survey_rec(user_id, time, etc)

    # Ryan: Figure out how to load a specific survey on the home page
    current_survey = "Do you like peanut butter or jelly?"
    option_a = "peanut butter"
    option_b = "jelly"
    # render text inside the buttons

    # Ryan: Record users survey choices to database

    return render_template('index.html', title='Home')


@app.route('/results')
def results():
    return render_template('results.html', title='Results')


@app.route('/magic')
def magic():
    return render_template('magic.html', title='Magic')


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


# DAVE added route for picking a survey option 

@app.route('/choose_survey', methods=["POST", "GET"])
def choose_survey():

    # We now have these variables for survey logic:
    selection = request.form['selection']
    current_user_first_name = request.form['current_user_first_name']

    output = "You picked: " + selection + " and you are logged in as: " + current_user_first_name
 
    return render_template("index.html", title='Home', messages={'main': output})
 

@app.route('/report_attribution', methods=["POST", "GET"])
def report_attribution():

    # We now have these variables for survey logic:
    if request.form['survey_id']:
        survey_id = request.form['survey_id']
    else:
        survey_id = 1
    if request.form['filter_is_verified']:
        filter_is_verified = request.form['filter_is_verified']
    else:
        filter_is_verified = 0


    # Define Filter State Dictionary for Results
    filter_state={}
    filter_state['verified'] = 1  # get from user.confirmation
    filter_state['geo'] = "United States"  # get from user.country
    filter_state['gender'] = "male"  # get from user.gender
    filter_state['age_range'] = "adult"  # bin into 10 or 20 years using: (current_time - user.birth_year)
    filter_state['date_range'] = "all"  # get from survey_responses.created_at

    # Perform discrete choice attribution calcs
    df_prep, list_options, option_index_list = attribution_calcs.prep_data_for_attribution_model(survey_id=survey_id, filter_state=filter_state)
    
    list_options, list_weights = attribution_calcs.compute_survey_attrib_weights(df_prep, list_options, option_index_list)
    
    output = "You picked survey_id: ", str(survey_id),\
     "  Options:  ", str(list_options),\
     "  Weighted Preferences:  ", str(list_weights)
    
    return render_template("results.html", title='Results', messages={'main': output})
 


# DAVE added route for similarity prediction

@app.route('/predict_sim', methods=["POST", "GET"])
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

    # return jsonify(dict_of_outputs)
    # return render_template('predict_sim.html', tables=[df_users.to_html(classes='data')], titles=df_users.columns.values)
    # return render_template('predict_sim.html', header='Similarity Results', content=str(jsonify(dict_of_outputs)))

    return render_template("magic.html", title='Magic', messages={'main': (dict_of_outputs)})
 
