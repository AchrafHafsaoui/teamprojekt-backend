##### STILL UNDER WORK

from DatabaseManager import DatabaseManager

class Station:
    def __init__(self, number: str, status: str, state_of_charge: float, electric_capacity: float, db_manager):
        self.number = number
        self.status = status
        self.state_of_charge = state_of_charge
        self.electric_capacity = electric_capacity
        self.db_manager = db_manager  # Inject DatabaseManager instance


    # Edit any station attribute dynamically
    def EditStation(self, param, value):    
        conn = self.db_manager.connect()
        if hasattr(self, param):
            setattr(self, param, value)
        cur = conn.cursor()
        cur.execute(
            f"UPDATE stations SET {param} = ? WHERE number = ?",
            (value, self.number)
        )
        conn.commit()
        print(f"Station '{self.number}' updated: {param} = {value}")


    # save the current station object to the database
    def save_to_database(self):
        conn = self.db_manager.connect()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO station_table (number, status, state_of_charge, electric_capacity) VALUES (?, ?, ?, ?)",
            (self.number, self.status, self.state_of_charge, self.electric_capacity)
        )
        conn.commit()
        print(f"Station '{self.number}' saved to database.")


    #  delet the current station object to the database
    def delete_from_database(self):
        conn = self.db_manager.connect()
        cur = conn.cursor()
        # Delete the station record where the number matches
        cur.execute("DELETE FROM station_table WHERE number = ?", (self.number,))
        conn.commit()
        print(f"Station '{self.number}' deleted from database.")


    # Fetch a station by parameter
    def fetch_station_through_params(self, param, value):
        conn = self.db_manager.connect()
        cur = conn.cursor()
        query = f"SELECT * FROM station_table WHERE {param} = ?"
        cur.execute(query, (value,))
        rows = cur.fetchall()
        if rows:
            print("bus_table found:")
            for row in rows:
                print(row)
        else:
            print(f"No station found with {param} = {value}.")


    # Fetch all stations 
    def fetch_all_station_data(self):
        conn = self.db_manager.connect()
        cur = conn.cursor()
        query = f"SELECT * FROM station_table "
        cur.execute(query)
        rows = cur.fetchall()
        if rows:
            print("bus_table found:")
            for row in rows:
                print(row)
        else:
            print(f"No station found with")




"""
# TESTING
# file need to always be executed in utils/ file in terminal
if __name__ == "__main__":
    # Files here or just in instance creation params
    db_file = '../data/data.db'  # Ensure the database file is created at the desired location
    table_name = 'station_table'

    # Create an instance of the stations manager only when establishing connection
    station_manager = Station("ST001", "Active", 0.1, 100.0, DatabaseManager(db_file)) 
    station_manager.save_to_database()
    station_manager.fetch_all_station_data()
    station_manager.delete_from_database()
"""