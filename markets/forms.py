
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Email,EqualTo,Length,DataRequired,ValidationError

from markets.models import User

class RegisterForm(FlaskForm):

    def validate_username(self,username_to_validate):
        user=User.query.filter_by(username=username_to_validate.data).first()
        if user:
            raise ValidationError("Username already exists.Please try some other username.")
    
    def validate_email(self,email_to_validate):
        user=User.query.filter_by(email=email_to_validate.data).first()
        if user:
            raise ValidationError("Email already exists.Please try some other username.")

    username=StringField(label="Username",validators=[Length(min=2,max=30),DataRequired()])
    email=StringField(label="Email",validators=[Email(),DataRequired()])
    password1=PasswordField(label="Password",validators=[Length(min=6),DataRequired()])
    password2=PasswordField(label="Password Confirmation",validators=[EqualTo('password1'),DataRequired()])
    submit=SubmitField(label="Register")


class LoginForm(FlaskForm):
    username=StringField(label="Username",validators=[DataRequired()])
    email=StringField(label="Email",validators=[Email(),DataRequired()])
    password=PasswordField(label="Password",validators=[DataRequired()])
    submit=SubmitField(label="Login")


class PurchaseForm(FlaskForm):
    submit=SubmitField(label="Purchase Item!")

class SellForm(FlaskForm):
    submit=SubmitField(label="Sell Item!")

