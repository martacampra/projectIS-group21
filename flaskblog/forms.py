from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, SelectField, TimeField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from flask_wtf.file import FileField, FileAllowed
from flaskblog.models import User
import re
import datetime

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
    #job=SelectField('Job', [DataRequired()], choices=[('Student', 'student'),('Teacher', 'teacher')])
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
    sport1 = SelectField('Sport', [DataRequired()], choices=[])
    level1 = SelectField('Level', [DataRequired()],
                         choices=[('never', 'Never'), ('beginner', 'Beginner'), ('intermediate', 'Intermediate'),
                                  ('advanced', 'Advanced')])
    sport2 = SelectField('Sport2', choices=[])
    level2 = SelectField('Level2',
                         choices=[('never', 'Never'), ('beginner', 'Beginner'), ('intermediate', 'Intermediate'),
                                  ('advanced', 'Advanced')])
    sport3 = SelectField('Sport3', choices=[])
    level3 = SelectField('Level3',
                         choices=[('never', 'Never'), ('beginner', 'Beginner'), ('intermediate', 'Intermediate'),
                                  ('advanced', 'Advanced')])
    submit = SubmitField('Update')


class CreateForm(FlaskForm):

    def validate_date(form, field):
        if field.data < datetime.date.today():
            raise ValidationError("The date cannot be in the past!")


    sport= SelectField('Sport', [DataRequired()], choices=[])
    level= SelectField('Level', [DataRequired()], choices=[('never', 'Never'), ('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')])
    place= SelectField('Place', [DataRequired()], choices=[])
    date= DateField('Date', format='%d-%m-%Y', validators=[DataRequired("Incorrect data format, should be DD-MM-YYYY")])
    time= TimeField('Time', format='%H:%M', validators=[DataRequired("Incorrect data format, should be HH:MM")])
    np= IntegerField('Number of participants needed', validators=[DataRequired()])
    cost= FloatField('Price [Euro]', validators=[DataRequired()])
    submit = SubmitField('Create')

class UpdatePlaceForm(FlaskForm):
    place=StringField('place', validators=[DataRequired()])
    submit= SubmitField('Update')

    def validate_place(self ):
        #controllo che il testo sia corretto
        pass




class CreateForm(FlaskForm):
    def validate_date(form, field):
        if field.data < datetime.date.today():
            raise ValidationError("Date cannot be in the past!")

    sport= SelectField('Sport', [DataRequired()], choices=[])
    level= SelectField('Level', [DataRequired()], choices=[('never', 'Never'), ('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')])
    place= SelectField('Place', [DataRequired()], choices=[])
    date= DateField('Date', format='%d-%m-%Y', validators=[DataRequired("incorrect data format, should be dd-mm-yyyy")])
    time= TimeField('Time', format='%H:%M', validators=[DataRequired("incorrect time format, should be HH:MM")])
    np= IntegerField('Number', validators=[DataRequired()])
    cost= FloatField('Price', validators=[DataRequired()])
    submit = SubmitField('Create')

class UpdatePlaceForm(FlaskForm):
    place=StringField('place', validators=[DataRequired()])
    submit= SubmitField('Update')

    def validate_place(self ):
        #controllo che il testo sia corretto
        pass
