from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired


class WatermarkForm(FlaskForm):
    image = FileField('image', validators=[FileRequired()])
