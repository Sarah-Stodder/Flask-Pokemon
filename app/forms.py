from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CatchPokemon(FlaskForm):
    pokemon_name = StringField("A Wild Pokemon Appears! Whats it's name?", validators=[DataRequired()])
    submit = SubmitField('Capture!')