from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm


class Find_pokemon(FlaskForm):
    pokemon_name = StringField("A Wild Pokemon Appears! Whats it's name?", validators=[DataRequired()])
    submit = SubmitField('Find!')