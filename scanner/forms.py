from flask_wtf import FlaskForm
from wtforms import SelectField, URLField
from wtforms.validators import DataRequired

from scanner.choices import ScanTypes


class ScanForm(FlaskForm):
    target_url = URLField(label='URL', validators=[DataRequired()])
    scan_type = SelectField(label='Type', validators=[DataRequired()], choices=ScanTypes.choices())
