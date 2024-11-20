#This is part of the utils, converts dummy csv data to a .db file
import pandas as pd
import sqlite3

class CSVtoDatabase:
    # Constructor
    def __init__(self, csv_file, db_file, table_name):
        self.csv_file = csv_file
        self.db_file = db_file
        self.table_name = table_name
        self.connection = None

    # Load the CSV file into a Pandas DataFrame.
    def load_csv(self):
        try:
            self.df = pd.read_csv(self.csv_file)
            print("CSV file loaded.")
            #print(self.df.head())  
        except FileNotFoundError:
            print(f"Error: File '{self.csv_file}' not found.")
            raise
        except Exception as e:
            print(f"An error occurred while reading the CSV: {e}")
            raise
    
    # Establish a connection to the SQLite database
    def connect_to_db(self):
        try:
            self.connection = sqlite3.connect(self.db_file)
            print(f"Connected to database '{self.db_file}' successfully.")
        except Exception as e:
            print(f"An error occurred while connecting to the database: {e}")
            raise

    # Save the df to SQL database
    def save_to_db(self):
        try:
            if self.df.empty:
                print("The DataFrame is empty.. Nothing to save.")
                return
            self.df.to_sql(self.table_name, self.connection, if_exists='replace', index=False)
            print(f"Data saved to table '{self.table_name}' in database '{self.db_file}'.")
        except Exception as e:
            print(f"An error occurred while saving data to the database: {e}")
            raise

    # Print the contents of the specified table
    def print_table(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name};")
            rows = cursor.fetchall()
            print(f"Contents of table '{self.table_name}':")
            for row in rows:
                print(row)
        except Exception as e:
            print(f"An error occurred while querying the database: {e}")
            raise

    # Close the database connection
    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed.")



# TESTING
# file need to always be executed in utils/ file in terminal
if __name__ == "__main__":
    # Files here or just in instance creation params
    csv_file = '../data/Electric_Bus_Simplified_Data.csv'
    db_file = '../data/data.db'  # Ensure the database file is created at the desired location
    table_name = 'bus_table'

    # Create an instance of the CSVtoDatabase class
    converter = CSVtoDatabase(csv_file, db_file, table_name)

    try:
        converter.load_csv()
        converter.connect_to_db()
        converter.save_to_db()
        converter.print_table()
    finally:
        converter.close_connection()

