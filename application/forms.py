from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, EmailField,StringField, IntegerField,PasswordField
from wtforms.validators import Length, InputRequired,Email, EqualTo,ValidationError, NumberRange
 

class LoginForm(FlaskForm):
    LoginUsername = StringField("Username:",validators=[InputRequired()])
    LoginPassword= PasswordField("Password",validators=[InputRequired()])
    submit = SubmitField("Login")

class SignUpForm(FlaskForm):
    UserName = StringField("UserName:",validators=[InputRequired(),Length(min=6)])
    Password= PasswordField("Password",validators=[InputRequired(),Length(min=6)])
    confirmPassword = PasswordField('Confirm Your Password',validators=[InputRequired(),EqualTo('Password')])
    submit = SubmitField("Sign Up")