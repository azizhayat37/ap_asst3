from data import *

from app import db


def populate_database():
    with open('data/file.txt', 'r') as file:
        # Read the contents of the file
        contents = file.read()
        
        # Iterate through the lines of the file and add them to the database