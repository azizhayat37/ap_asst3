from app import app, db
from flask import request, render_template, flash, redirect, url_for
from data_loader import populate_database, create_chart
from forms import ChartDateForm
from models import IndexData
from datetime import datetime

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ChartDateForm()
    # renders a homepage and a stock chart
    start_date = datetime(2001, 1, 3)
    end_date = datetime(2013, 4, 8)
    date_options = IndexData.query.with_entities(IndexData.date).all()
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
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