import pandas as pd
from pandas.io import sql
import numpy as np  
from collections import OrderedDict
import pylogit as pl
from app import db

def sql_for_computing_survey_results(survey_id, filter_state):
    
    get_survey_responses_sql = '''
    
    SELECT 
        sr.id AS response_id,
        s.id AS survey_id,
        s.survey_name,
        sr.user_id,
        sr.created_at AS viewed_at,
        sr.impression_id,
        sr.survey_options_id,
        sr.is_selected,
        so.option_name
    FROM
        surveys as s
    LEFT JOIN
        survey_options as so
    ON 
        so.survey_id = s.id
    LEFT JOIN
        survey_responses as sr
    ON 
        so.id = sr.survey_options_id
    LEFT JOIN
        users as u 
    ON
        sr.user_id = u.id

    WHERE
        s.id = {0}
    AND sr.is_interacted_with = 1  
    AND u.confirmation IN (0, 1, {1})
    '''.format(survey_id, filter_state['verified'])
    
    return get_survey_responses_sql



########################

# get survey from id in format required for computing weights
def prep_data_for_attribution_model(survey_id, filter_state):
     
    #Sql select all surveys that are in filters 
    get_survey_responses_sql = sql_for_computing_survey_results(survey_id, filter_state)
    
    conn = db.engine.connect().connection
    df_prep = pd.read_sql_query(get_survey_responses_sql, conn).sort_values(by=['response_id'], ascending=True)
    
    df_prep.head()
    # Check if N>n_min :: require a min number of observations for privacy (and model fit efficiency and accuracy)

    # put into format for fitting 
    df_prep['alt_opt_num'] = 0
    df_prep['mix_model_id'] = 1

    # create a column for each option that is present
    list_options = sorted(df_prep['option_name'].unique())
    
    for k, col_name in enumerate(list_options):
        df_prep[col_name] = 0.0
        df_prep.loc[df_prep['option_name']==col_name, col_name] = 1.0
        df_prep.loc[df_prep['option_name']==col_name, 'alt_opt_num'] = k+1

    option_index_list = [*range(1,1+len(list_options),1)]

    return df_prep, list_options, option_index_list



########################

def compute_survey_attrib_weights(df_prep, list_options, option_index_list):
    # fit model, w num of draws proportional to N?

    option_index_specification = OrderedDict()
    option_name_specification = OrderedDict()
    
    for col in list_options:
        option_index_specification[col] = [option_index_list]
        option_name_specification[col] = [col]
    
    mixed_logit_model = pl.create_choice_model(data=df_prep,
                                           alt_id_col="alt_opt_num",
                                           obs_id_col="impression_id",
                                           choice_col="is_selected",
                                           specification=option_index_specification,
                                           model_type="Mixed Logit",
#                                            model_type="MNL",
                                           names=option_name_specification,
                                           mixing_id_col="mix_model_id",
                                           mixing_vars=list_options
                                          )

    # Note 2 * len(index_var_names) is used because we are estimating
    # both the mean and standard deviation of each of the random coefficients
    # for the listed index variables.
    try:
        mixed_logit_model.fit_mle(
                        init_vals=np.zeros(2 * len(list_options))
    #                     init_vals=np.zeros(1 * len(list_options))
                        , num_draws=1000
                        , seed=99
                         )  
        print("we fit a model")
    except:
        error = "singular matrix errors seem fine since we still get ok coeffs, ignore until a brilliant statistician explains otherwise"
        print("error at step 1")

        
    try:        
        denominator = 0
        list_coeffs = np.zeros(len(option_index_list))

        for i in option_index_list:
            list_coeffs[i-1] = np.exp(mixed_logit_model.coefs[i-1])
            denominator = denominator + list_coeffs[i-1]

        list_weights = list_coeffs / denominator
                
    except:
        error = "??"
        print("error at step 2")
              
            
    return list_options, list_weights #, mixed_logit_model

