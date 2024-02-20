from app import app
from flask import request, render_template, flash, redirect, url_for
from data_loader import populate_database

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('landing_page.html')

@app.route('/test_data_loader', methods=['GET', 'POST'])
def test_data_loader():
    populate_database()
    return 'Now testing the data loader...'