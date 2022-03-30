from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import (Required, Length, ValidationError,
                                EqualTo)
from app.models import Survey, SurveyOptions


class CreateSurvey(Form):

    ''' Create Survey Form. '''

    survey_name = TextField(validators=[Required(), Length(min=2)],
                     description='survey_name')
    created_by_user_id = TextField(validators=[Required(), Length(min=1)],
                      description='created_by_user_id (make this automatic in future)')
    option1 = TextField(validators=[Required(), Length(min=1)],
                     description='option1')
    option2 = TextField(validators=[Required(), Length(min=1)],
                     description='option2')
    option3 = TextField(validators=[Length(min=0)],
                     description='option3 (optional)')
    option4 = TextField(validators=[Length(min=0)],
                     description='option4 (optional)')
    option5 = TextField(validators=[Length(min=0)],
                     description='option5 (optional)')
    option6 = TextField(validators=[Length(min=0)],
                     description='option6 (optional)')
    option7 = TextField(validators=[Length(min=0)],
                     description='option7 (optional)')
    option8 = TextField(validators=[Length(min=0)],
                     description='option8 (optional)')
