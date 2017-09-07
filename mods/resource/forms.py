from flask_wtf import FlaskForm
from wtforms import StringField, validators
from wtforms.fields.html5 import DateField


class DownloadForm(FlaskForm):
    symbol = StringField('symbol', [validators.DataRequired()])
    contract_from = DateField(
        'contract_from',
        [validators.DataRequired()],
        format='%Y-%m-%d'
    )
    contract_to = DateField(
        'contract_to',
        [validators.DataRequired()],
        format='%Y-%m-%d'
    )
