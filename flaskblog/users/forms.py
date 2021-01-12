from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from flask_wtf.file import FileField, FileAllowed
from flaskblog.models import User


class AddSport(FlaskForm):
    sport1 = SelectField('Sport', [DataRequired()], choices=[])
    level1 = SelectField('Level', [DataRequired()],
                        choices=[('never', 'Never'), ('beginner', 'Beginner'), ('intermediate', 'Intermediate'),
                                 ('advanced', 'Advanced')])
    add = SubmitField('Add')


class LoginForm(FlaskForm):
    email= StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password', validators=[DataRequired()])
    remember=BooleanField('Remember me')
    submit=SubmitField('Login')


class RegistrationForm(FlaskForm):
    name=StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])#, Regexp('^[A-Za-z]*$','Name must have only letters')])
    surname=StringField('Surname', validators=[DataRequired(), Length(min=2, max=30)])#, Regexp('^[A-Za-z]*$','Surname must have only letters')])
    birthdate=DateField('Birthdate', format='%d-%m-%Y', validators=[DataRequired("Incorrect data format, should be DD-MM-YYYY")])
    email= StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30), Regexp('^.*(?=.*\d)(?=.*[a-z])'
                        '(?=.*[A-Z])(?=.*[!$%&#=?]).*$', message='Password must include at least one uppercase character, one digit and one special character (!$%&#=?).')])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])

    submit=SubmitField('Sign up')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered. Please choose a different one.')


class UpdateProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])#, Regexp('^[A-Za-z]*$','Name must have only letters')])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=30)])  # , Regexp('^[A-Za-z]*$','Surname must have only letters')])
    birthdate = DateField('Birthdate', format='%d-%m-%Y', validators=[DataRequired("Incorrect data format, should be DD-MM-YYYY")])
    email = StringField('Email', validators=[DataRequired(), Email()])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
