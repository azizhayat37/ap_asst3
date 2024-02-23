from app import app, db
from flask import request, render_template, flash, redirect, url_for
from data_loader import populate_database, create_chart
from forms import ChartDateForm
from models import IndexData
from datetime import datetime
from sqlalchemy import extract

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ChartDateForm()

    #create the database if it doesn't exist
    try:
        test_query = IndexData.query.first()
        if test_query is None:
            populate_database()
        else:
            print("Database exists")
    except Exception as e:
        print(e)

    # dates in the dropdown menus come from the database, 1st of month only
    date_options = IndexData.query.with_entities(IndexData.date).filter(extract('day', IndexData.date) == 1).all() # get the first of every month
    date_options = [(date.date, date.date) for date in date_options]  # adjust date format to get rid of parentheses
    form.start_date.choices, form.end_date.choices = date_options, date_options

    # default starting and ending dates - show the entire time span
    start_date = datetime(2001, 1, 3)
    end_date = datetime(2013, 4, 8)

    # upon submitting the form, get the user's selected dates
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
    
    # create the chart that renders as soon as you hit the page
    chart = create_chart(start_date, end_date)
    
    return render_template('index.html', chart=chart, form=form, date_options=date_options)

@app.route('/test', methods=['GET', 'POST'])
def test():
    try:
        #uncomment lines below as necessary to test certain parts of the code
        #populate_database()
        start_date = datetime(2001, 1, 3)
        end_date = datetime(2001, 1, 28)
        test_query = IndexData.query.filter(IndexData.date >= start_date, IndexData.date <= end_date).all()
        print("Printing a test query...")
        print(test_query)
    except Exception as e:
        print(e)
    return 'Now testing the data loader...'