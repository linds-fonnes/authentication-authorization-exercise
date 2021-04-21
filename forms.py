from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired,Email,Length

class UserRegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20, message="Max Character Length: 20")])

    password = PasswordField("Password", validators=[InputRequired()])
    
    email = StringField("Email", validators=[InputRequired(), Email(message="Please input valid email address"), Length(min=1,max=50,message="Max Character Length: 50")])

    first_name = StringField("First Name", validators=[InputRequired(), Length(min=1, max=30, message="Max Character Length: 30")])

    last_name = StringField("Last Name", validators=[InputRequired(), Length(min=1,max=30,message="Max Character Length: 30")])

class UserLoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20, message="Max Character Length: 20")])

    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(min=1, max=100, message=" Max Character Length: 100")])
    content = StringField("Content", validators=[InputRequired()])
