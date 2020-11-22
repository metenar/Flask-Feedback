from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email

class UserForm(FlaskForm):
    username=StringField('Username',validators=[InputRequired(),Length(min=3,max=20,message="Your username too long/short")])
    password=PasswordField('Password',validators=[InputRequired()])
    email=StringField('Email',validators=
        [InputRequired(),Length(min=5,max=50,message="Your Email too long/short")])
    first_name=StringField('First Name',validators=[InputRequired(),Length(min=3,max=30,message="Your First name too long/short")])
    last_name=StringField('Last Name',validators=[InputRequired(), Length(min=3,max=30,message="Your Last name too long/short")])

class LoginForm(FlaskForm):
    username=StringField('Username',validators=[InputRequired()])
    password=PasswordField('Password',validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    title=StringField('Title of Feedback',validators=[InputRequired(),Length(min=5,max=100,message="Your Title too long/short")])
    content=StringField('Content of Feedback', validators=[InputRequired()])
