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


def populate_database(ID):
    # the source of the data:
    # SP500: https://www.kaggle.com/datasets/rupindersinghrana/us-stock-price-index-over-17912015
    # VIX: https://www.cboe.com/tradable_products/vix/vix_historical_data/

    if ID == 'SP500':
        file_name = 'data/SP_PRICE_INDEX_US.csv'
    elif ID == 'VIX':
        file_name = 'data/VIX_DATA.csv'

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
                    ticker=str(line[1]), 
                    open=float(line[2]), 
                    high=float(line[3]), 
                    low=float(line[4]), 
                    close=float(line[5])
                )
            elif ID == 'VIX':
                index_data = VIXData(
                    date=formatted_date,
                    open=float(line[2]), 
                    high=float(line[3]), 
                    low=float(line[4]), 
                    close=float(line[5])
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

    # set figure title
    fig.update_layout(title=f'{ID} Price Over Time')

    return fig.to_html(full_html=False)


