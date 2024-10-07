from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField , PasswordField , BooleanField
from wtforms.validators import DataRequired ,length ,Email, Regexp ,EqualTo

################################################################
class registrationForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired() , length(min=2, max=25)])
    lname = StringField('Last Name', validators=[DataRequired() , length(min=2, max=25)])
    username = StringField('Username', validators=[DataRequired() , length(min=2, max=25)])
    email = StringField('Email', validators=[DataRequired() ,Email()])
    password = PasswordField('Password', validators=[DataRequired() , Regexp(r'^[A-Za-z0-9@#$%^&+=]{8,}', message='Password must contain at least 8 characters')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired() , EqualTo('password', message='Passwords must match')])
    gender = BooleanField('Gender', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
################################################################
class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired() ,Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
 


