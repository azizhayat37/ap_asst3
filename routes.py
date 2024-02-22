from app import app
from flask import request, render_template, flash, redirect, url_for
from data_loader import populate_database, create_chart

@app.route('/', methods=['GET', 'POST'])
def index():
    chart = chart = create_chart(start_date='2001-01-01', end_date='2001-12-31')
    return render_template('index.html', chart=chart)

@app.route('/test_data_loader', methods=['GET', 'POST'])
def test_data_loader():
    populate_database()
    return 'Now testing the data loader...'