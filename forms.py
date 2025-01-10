from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class StationSelectionForm(FlaskForm):
    station_id = SelectField('Select a Station:', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')
