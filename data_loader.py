from data import *
from app import db
from models import IndexData
import csv


def populate_database():
    with open('data/SP_PRICE_INDEX_US.csv', 'r') as file:
        # Read the contents of the file
        csv_reader = csv.reader(file)
        # Skip the header line
        next(csv_reader)
        # Iterate through the lines of the file and use the to create a new IndexData object
        for line in file:
            # Process each line and add it to the database
            index_data = IndexData(
                date=str(line[0]), 
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
