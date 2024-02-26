from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo

class ChartDateForm(FlaskForm):
    # accept user input to amend the start and end dates of the stock chart
    start_date = SelectField('Start Date', validators=[DataRequired()])
    end_date = SelectField('End Date', validators=[DataRequired()])
    submit = SubmitField('Submit')
    

class PortfolioUpdateForm(FlaskForm):
    asset_choice = SelectField('Asset', validators=[DataRequired()])
    quantity = SelectField('Quantity', validators=[DataRequired()])
    add_subtract = RadioField('Add/Subtract', validators=[DataRequired()])
    submit = SubmitField('Submit')