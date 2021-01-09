from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, SelectField, TimeField, IntegerField, FloatField
from wtforms.validators import DataRequired, ValidationError
import datetime


#class AddSport(FlaskForm):
    #sport1 = SelectField('Sport', [DataRequired()], choices=[])
    #level1 = SelectField('Level', [DataRequired()],
                         #choices=[('never', 'Never'), ('beginner', 'Beginner'), ('intermediate', 'Intermediate'),
                                 # ('advanced', 'Advanced')])

    #add = SubmitField('Add')


class CreateForm(FlaskForm):

    def validate_date(form, field):
        if field.data < datetime.date.today():
            raise ValidationError("The date cannot be in the past!")


    sport = SelectField('Sport', [DataRequired()], choices=[])
    level= SelectField('Level', [DataRequired()], choices=[('never', 'Never'), ('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')])
    place= SelectField('Place', [DataRequired()], choices=[])
    date= DateField('Date', format='%d-%m-%Y', validators=[DataRequired("Incorrect data format, should be DD-MM-YYYY")])
    time= TimeField('Time', format='%H:%M', validators=[DataRequired("Incorrect data format, should be HH:MM")])
    np= IntegerField('Number of participants needed', validators=[DataRequired()])
    cost= FloatField('Price [Euro]', validators=[DataRequired()])
    submit = SubmitField('Create')


#class UpdatePlaceForm(FlaskForm):
    #place=StringField('place', validators=[DataRequired()])
   # submit= SubmitField('Update')

    #def validate_place(self ):
        #controllo che il testo sia corretto
     #   pass
