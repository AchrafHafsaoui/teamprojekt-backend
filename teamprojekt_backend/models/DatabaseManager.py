# This is a temporary implementation for DB connection management for the different DBs
##### STILL UNDER WORK

import sqlite3

class DatabaseManager:
    _instances = {}

    # Singleton pattern to ensure only one instance per database file
    # add the .db file name when calling this function
    def __new__(cls, db_file):
        if db_file not in cls._instances:
            instance = super().__new__(cls)
            instance._initialize(db_file)
            cls._instances[db_file] = instance
        return cls._instances[db_file]

    # Initialize the database connection
    def _initialize(self, db_file):
        self.db_file = db_file
        self.connection = None

    # Create or return the existing database connection
    def connect(self):
        if not self.connection:
            self.connection = sqlite3.connect(self.db_file)
            print(f"Connected to database: {self.db_file}")
        return self.connection

    # Close the database connection
    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print(f"Database connection closed: {self.db_file}")

    # Check if the database connection is active, True if active, False otherwise
    def check_connection(self):
        return self.connection is not None



# TESTING
# file need to always be executed in utils/ file in terminal
if __name__ == "__main__":
    # Files here or just in instance creation params
    db_file = '../data/Bus_data.db'  # Ensure the database file is created at the desired location
    table_name = 'bus_table'

    # Create an instance of the DB manager only when establishing connection
    db_manager = DatabaseManager(db_file)

    conn = db_manager.connect()

