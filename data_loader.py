from data import *
from app import db
from models import IndexData
import csv
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

def populate_database():
    # the source of the data is Kaggle:
    # https://www.kaggle.com/datasets/rupindersinghrana/us-stock-price-index-over-17912015

    with open('data/SP_PRICE_INDEX_US.csv', 'r') as file:
        # Read the contents of the file
        csv_reader = csv.reader(file)
        # Skip the header line
        next(csv_reader)

        for line in csv_reader:
            # Convert date from MM/DD/YYYY to YYYY-MM-DD format
            formatted_date = datetime.strptime(line[0], '%m/%d/%Y').strftime('%Y-%m-%d')

            # Process each line and add it to the database
            index_data = IndexData(
                date=formatted_date, 
                ticker=str(line[1]), 
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


def create_chart(start_date, end_date):
    # load the stock data for the time period selected by the user
    df = pd.read_sql(IndexData.query.filter(IndexData.date.between(start_date, end_date)).statement, db.engine,
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
    fig.update_layout(title='SP500 Index Price Over Time')

    return fig.to_html(full_html=False)