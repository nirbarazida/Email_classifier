from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, optional, ValidationError
from spam_or_ham_classifier.web_database.ORM import UserTable


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=15)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    email = StringField('Email', validators=[Email(), DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        if UserTable.query.filter_by(username=username.data).first():
            raise ValidationError(f'User name exist in the system. please choose different username')

    def validate_email(self, email):
        if UserTable.query.filter_by(email_address=email.data).first():
            raise ValidationError(f'email address exist in the system. please choose different username')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=15)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class ClassificationForm(FlaskForm):
    email_title = StringField('Title', validators=[optional()])
    email_cont = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Classify')
