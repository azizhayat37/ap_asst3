from data import *
from app import db
from models import IndexData, VIXData, Portfolio, Assets
import csv
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

def check_databases_exist():
    #check that the databases to be populated from CSV exist, otherwise create them
    databases = {'SP500': IndexData, 'VIX': VIXData}

    for ID, database in databases.items():
        try:
            test_query = database.query.first()
            if test_query is None:
                populate_database(ID)
        except Exception as e:
            print(f"Error in check_databases_exist()... {ID} DATABASE AFFECTED")
            print(e)

    # check that the Assets & Portfolio databases are populated, otherwise create it
    if Assets.query.first() is None:
        for ID in databases.keys():
            asset = Assets(ticker=ID)
            asset.determine_full_name(ID)
            db.session.add(asset)
        db.session.commit()

    if Portfolio.query.first() is None:
        for asset in Assets.query.all():
            holding = Portfolio(asset_id=asset.id, quantity=0)
            holding.determine_ticker(asset.id)
            db.session.add(holding)
        db.session.commit()


def populate_database(ID):
    # the source of the data in /data is Kaggle and CBOE, respectively:
    # SP500: https://www.kaggle.com/datasets/rupindersinghrana/us-stock-price-index-over-17912015
    # VIX: https://www.cboe.com/tradable_products/vix/vix_historical_data/

    # designate the file to be read
    if ID == 'SP500':
        file_name = 'data/SP_PRICE_INDEX_US.csv'
    elif ID == 'VIX':
        file_name = 'data/VIX_History.csv'

    with open(file_name, 'r') as file:
        # Read the contents of the file
        csv_reader = csv.reader(file)
        # Skip the header line
        next(csv_reader)

        for line in csv_reader:
            # Convert date from MM/DD/YYYY to YYYY-MM-DD format
            formatted_date = datetime.strptime(line[0], '%m/%d/%Y').strftime('%Y-%m-%d')

            # Process each line and add it to the database as per the ID
            if ID == 'SP500':
                index_data = IndexData(
                    date=formatted_date, 
                    ticker='SP500', 
                    open=float(line[2]), 
                    high=float(line[3]), 
                    low=float(line[4]), 
                    close=float(line[5])
                )
            elif ID == 'VIX':
                index_data = VIXData(
                    date=formatted_date,
                    ticker='VIX',
                    open=float(line[1]), 
                    high=float(line[2]), 
                    low=float(line[3]), 
                    close=float(line[4])
                )

            # Add the new IndexData object to the database
            db.session.add(index_data)
        # Commit the changes to the database
        db.session.commit()
        # Close the file
        file.close()


def create_chart(start_date, end_date, ID):
    # load the stock data for the time period selected by the user
    if ID == 'SP500':
        df = pd.read_sql(IndexData.query.filter(IndexData.date.between(start_date, end_date)).statement, db.engine,
            index_col='date'
        )
    elif ID == 'VIX':
        df = pd.read_sql(VIXData.query.filter(VIXData.date.between(start_date, end_date)).statement, db.engine,
            index_col='date'
        )

    # create a line chart of the stock data
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index, 
        y=df['close'], 
        mode='lines'
    ))

    # prefix y-axis tick labels with dollar sign
    fig.update_yaxes(tickprefix="$")

    # Set figure title and size
    fig.update_layout(
        title='',
        width=1200,  # Set the width
        height=600   # Set the height
    )

    chart_title = Assets.query.filter_by(ticker=ID).first().full_name
    # set figure title
    fig.update_layout(title=str(chart_title) + ' Price Chart')

    return fig.to_html(full_html=False)

def create_double_chart(start_date, end_date):
    # load the SP500 data for the time period selected by the user
    SP500 = pd.read_sql(IndexData.query.filter(IndexData.date.between(start_date, end_date)).statement, db.engine,
        index_col='date'
    )

    # load the VIX data for the time period selected by the user
    VIX = pd.read_sql(VIXData.query.filter(VIXData.date.between(start_date, end_date)).statement, db.engine,
        index_col='date'
    )

    # create a line chart for SP500
    sp500_trace = go.Scatter(
        x=SP500.index, 
        y=SP500['close'], 
        mode='lines',
        name='SP500'
    )

    # create a line chart for VIX
    vix_trace = go.Scatter(
        x=VIX.index, 
        y=VIX['close'], 
        mode='lines',
        name='VIX',
        yaxis='y2'  # Assign the trace to the right y-axis
    )

    # create a figure and add the traces
    fig = go.Figure()
    fig.add_trace(sp500_trace)
    fig.add_trace(vix_trace)

    # prefix y-axis tick labels with dollar sign
    fig.update_yaxes(tickprefix="$")

    # Set figure title and size
    fig.update_layout(
        title='',
        width=1200,  # Set the width
        height=600   # Set the height
    )

    # set figure title
    fig.update_layout(title='SP500 & VIX Price Chart')

    # Add a right y-axis for VIX
    fig.update_layout(
        yaxis2=dict(
            title='VIX',
            overlaying='y',
            side='right',
            tickprefix='$'
        ),
        yaxis=dict(
            title='SP500',
            tickprefix='$'
        )
    )

    # Set the legend position to top center (otherwise it covers the right-side y-axis ticks)
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.0,
        xanchor="center",
        x=0.5
    ))

    return fig.to_html(full_html=False)

def update_portfolio(asset_choice, quantity):
    # check if the asset is already in the portfolio, if not, add it and amend quantity
    asset_possibilities = ['SP500', 'VIX']
    asset_object = Assets.query.filter_by(ticker=asset_choice).first()

    if asset_object:
        # Extract the id (or another relevant field) from the Assets object
        asset_id = asset_object.id
    
    # if the asset isn't in the portfolio, create it, otherwise just update portfolio holdings
    if asset_choice in asset_possibilities:
        asset = Portfolio.query.filter_by(asset_id=asset_id).first()
        if asset is None:
            asset = Portfolio(asset_id=asset_id, quantity=quantity)
            db.session.add(asset)
        else:
            #this cannot go negative as selection is limited in the dropdown list
            asset.quantity = quantity
        db.session.commit()

#DATES MUST BE IN THIS FORMAT --> end_date.strftime('%Y-%m-%d')
def generate_investment_data(ticker, start_date, end_date):

    # determine the database beed to be queried
    if ticker == 'SP500':
        target_db = IndexData
    elif ticker == 'VIX':
        target_db = VIXData

    # get/calculate data need for the boxes below the rendered chart
    etf_name = Assets.query.filter_by(ticker=ticker).first().full_name
    asset_id = Assets.query.filter_by(ticker=ticker).first().id
    position = Portfolio.query.filter_by(asset_id=asset_id).first().quantity
    entry_price = target_db.query.filter_by(date=start_date).first().close
    exit_price = target_db.query.filter_by(date=end_date).first().close
    profit_loss = round((exit_price * position) - (entry_price * position), 2)

    return etf_name, position, entry_price, exit_price, profit_loss
