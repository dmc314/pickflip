from flask import (Blueprint, render_template, redirect, request, url_for,
                   abort, flash)
from itsdangerous import URLSafeTimedSerializer
from app import app, models, db
from app.models import Survey, SurveyOptions
from app.forms import survey as survey_forms
from sqlalchemy import func

# Create a survey blueprint
surveybp = Blueprint('surveybp', __name__, url_prefix='/survey')


# Function to Create a New Survey
@surveybp.route('/create_survey', methods=['GET','POST'])
def create_survey():
    form = survey_forms.CreateSurvey()
    if form.validate_on_submit():
    
        # Create a survey with options
        survey_name=form.survey_name.data,
        created_by_user_id=form.created_by_user_id.data,
        
        survey_options_list=[]
        survey_options_list.append(form.option1.data)
        survey_options_list.append(form.option2.data)
        
        if form.option3.data:
            survey_options_list.append(form.option3.data)
        if form.option4.data:
            survey_options_list.append(form.option4.data)
        if form.option5.data:
            survey_options_list.append(form.option5.data)
        if form.option6.data:
            survey_options_list.append(form.option6.data)
        if form.option7.data:
            survey_options_list.append(form.option7.data)
        if form.option8.data:
            survey_options_list.append(form.option8.data)

        new_survey = Survey(survey_name=survey_name, created_by_user_id=created_by_user_id)
        db.session.add(new_survey)
        db.session.commit()

        # DMC Get the current or max survey_id so we can link the options to it
        # This may not be robust forever if we have concurrent users...need to pass a UUID generated here at the same time to both tables
        max_survey_id = db.session.query(func.max(Survey.id)).scalar()
        
        for option in survey_options_list:
            new_survey_option = SurveyOptions(survey_id=max_survey_id, option_name=option)
            db.session.add(new_survey_option)
    
        # Insert the survey and survey_options into the database
        db.session.commit()
        
        flash('Added survey to database!', 'positive')

        return redirect(url_for('index'))
    return render_template('survey/create_survey.html', form=form, title='Create Survey')
 


