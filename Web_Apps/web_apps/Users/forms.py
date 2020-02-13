#Flask forms & validators
from flask_wtf import FlaskForm
from wtforms import  StringField, SubmitField, DateField, ValidationError, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
#from wtforms_alchemy import ModelForm  #For sqlalchemy related validations (like uniqueness of fields)
from web_apps.models import User


class signInForm(FlaskForm):
    email = StringField("Email", validators = [Email(message="Please enter a correct email"), DataRequired()])
    password = PasswordField("Password", validators= [DataRequired()])
    login = SubmitField(label = "Login")
    
    
class signUpForm(FlaskForm):
    name = StringField("Full Name", validators = [DataRequired(message= "Please provide a name")])
    email = StringField("Email", validators = [Email(message="Please enter a correct email")])
    pseudo = StringField("User Name", validators = [DataRequired(message= "Please provide a username")])
    birthdate = DateField("Birth Date", format="%d/%m/%Y")
    password = PasswordField("Password", validators= [DataRequired(), EqualTo('password_conf', message="Passwords must match")])
    password_conf = PasswordField("Password Confirmation", validators= [DataRequired()])
    create = SubmitField(label = "Create Account")
    
    def check_email_new(self, field):
        if User.query.filter_by(email=field.data).first():
            raise(ValidationError("Your email already exists"))
            
    def check_pseudo_new(self, field):
        if User.query.filter_by(pseudo=field.data).first():
            raise(ValidationError("Your pseudo already taken"))
        
    
    
class modifyForm(FlaskForm):
    pseudo = StringField("New User Name", validators = [DataRequired(message= "Please provide a username")])
    password = PasswordField("New Password", validators= [DataRequired(), EqualTo('password_conf', message="Passwords must match")])
    password_conf = PasswordField("New Password Confirmation", validators= [DataRequired()])
    apply = SubmitField(label = "Apply modifications")

class deleteForm(FlaskForm):
    delete = SubmitField("Delete Account")
    
    
    




