from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField
from wtforms.validators import DataRequired, regexp

class HabitForm(FlaskForm):
    habit = StringField('habit', validators=[regexp(r'\b.{3,}', message="Habit must contain three(3) or more characters")])
    date_started = DateTimeField('date_started', validators=[DataRequired()])

class HabitCompletedForm(FlaskForm):
    habit = StringField('habit', validators=[regexp(r'\b[0-9A-f]{24}\b', message="habit must be of type objectid")])
    date_completed = DateTimeField('date_completed', validators=[DataRequired()])
