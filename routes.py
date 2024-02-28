from app import app, db
from flask import request, render_template, flash, redirect, url_for
from data_loader import create_chart, check_databases_exist, update_portfolio, generate_investment_data
from forms import ChartDataForm, PortfolioUpdateForm
from models import IndexData, VIXData, Assets, Portfolio
from datetime import datetime
from sqlalchemy import extract

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ChartDataForm()

    #create the database if it doesn't exist
    check_databases_exist()
    
    # default starting and ending dates - show the entire time span
    start_date = datetime(2001, 1, 3)
    end_date = datetime(2013, 4, 8)

    # dates in the dropdown menus come from the database, 1st of month only
    date_options = IndexData.query.with_entities(IndexData.date).filter(extract('day', IndexData.date) == 1).all() # get the first of every month
    date_options = [(date.date, date.date) for date in date_options]  # adjust date format to get rid of parentheses
    form.start_date.choices, form.end_date.choices = date_options, date_options

    etf_name, position, entry_price, exit_price, profit_loss = generate_investment_data('VIX', start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

    # upon submitting the form, get the user's selected dates
    if form.validate_on_submit():
        # create the data that will populare the boxes beneath the chart
        start_date = form.start_date.data
        end_date = form.end_date.data
        etf_name, position, entry_price, exit_price, profit_loss = generate_investment_data('VIX', start_date, end_date)
    
    # create the chart that renders as soon as you hit the page
    chart = create_chart(start_date, end_date, 'SP500')

    return render_template('index.html', chart=chart, form=form, date_options=date_options, etf_name=etf_name, position=position, 
                           entry_price=entry_price, exit_price=exit_price, profit_loss=profit_loss)


@app.route('/volatility', methods=['GET', 'POST'])
def volatility():
    form = ChartDataForm()

    # default starting and ending dates - show the entire time span
    start_date = datetime(2001, 1, 3)
    end_date = datetime(2013, 4, 8)

    # dates in the dropdown menus come from the database, 1st of month only
    date_options = VIXData.query.with_entities(VIXData.date).filter(extract('day', VIXData.date) == 1).all() # get the first of every month
    date_options = [(date.date, date.date) for date in date_options]  # adjust date format to get rid of parentheses
    form.start_date.choices, form.end_date.choices = date_options, date_options

    etf_name, position, entry_price, exit_price, profit_loss = generate_investment_data('VIX', start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

    # upon submitting the form, get the user's selected dates
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        etf_name, position, entry_price, exit_price, profit_loss = generate_investment_data('VIX', start_date, end_date)
    
    # create the chart that renders as soon as you hit the page
    chart = create_chart(start_date, end_date, 'VIX')
    
    return render_template('index.html', form=form, chart=chart, date_options=date_options, etf_name=etf_name, position=position, 
                           entry_price=entry_price, exit_price=exit_price, profit_loss=profit_loss)


@app.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
    form = PortfolioUpdateForm()

    # Establish the dropdown menu options
    asset_choices = [("SP500", "SP500"), ("VIX", "VIX")]
    quantity_choices = [(str(i), str(i)) for i in range(1, 101)]  # Ensure choices are in a format suitable for the form
    form.asset_choice.choices, form.quantity.choices = asset_choices, quantity_choices

    # query user portfolio
    portfolio = db.session.query(Portfolio, Assets).join(Assets, Portfolio.asset_id == Assets.id).all()

    # update the user's portfolio once the form is submitted
    if form.validate_on_submit():
        update_portfolio(
            asset_choice=form.asset_choice.data, 
            quantity=int(form.quantity.data)
        )
    
    return render_template('portfolio.html', form=form, portfolio=portfolio)


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
