from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.login import UserMixin

from app import db, bcrypt


class User(db.Model, UserMixin):

    ''' A user who has an account on the website. '''

    __tablename__ = 'users'

# Ryan or Abeer - generate user_uuid and put in db. Want to call this here too.
# Also need to figure out generically how to query and write to the database

    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone = db.Column(db.String)
    email = db.Column(db.String, primary_key=True)
    confirmation = db.Column(db.Boolean)
    paid = db.Column(db.Boolean)
    _password = db.Column(db.String)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def check_password(self, plaintext):
        return bcrypt.check_password_hash(self.password, plaintext)

    def get_id(self):
        return self.email

    def is_paid(self):
        return self.paid



class Survey(db.Model):

    ''' A survey '''

    __tablename__ = 'surveys'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    survey_name = db.Column(db.String)
    survey_keywords = db.Column(db.String)
    survey_vector = db.Column(db.String)
    created_by_user_id = db.Column(db.Integer)
    
    def __repr__(self):  # How it is called/represented
        return '<Survey {0}, {1}>'.format(self.id, self.survey_name)


class SurveyOptions(db.Model):

    ''' The Options in a specific survey '''

    __tablename__ = 'survey_options'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    survey_id = db.Column(db.String) # DMC Add foreign key constraint?
    option_name = db.Column(db.String)
    
    def __repr__(self):  # How it is called/represented
        return '<Survey Option {0}, {1}>'.format(self.id, self.option_name)
