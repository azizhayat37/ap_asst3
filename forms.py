from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo


class ChartDataForm(FlaskForm):
    # accept user input to amend the start and end dates of the stock chart being rendered by plotly
    start_date = SelectField('Start Date', validators=[DataRequired()])
    end_date = SelectField('End Date', validators=[DataRequired()])
    submit = SubmitField('Submit')
    

class PortfolioUpdateForm(FlaskForm):
    # accept user input to update the holdings of ETFs in their portfolio
    asset_choice = SelectField('Asset', validators=[DataRequired()])
    quantity = SelectField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Submit')