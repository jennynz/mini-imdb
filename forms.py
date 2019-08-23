from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired

class Select_Movie(FlaskForm):
    movies = SelectField('movies', validators=[DataRequired(message="Didn't enter any data")], coerce=int)
