##### STILL UNDER WORK

class Bus:

    def __init__(self, license_plate: str, date_of_purchase: str, status: str, 
                 state_of_charge: float, electric_capacity: float, seat_capacity: int):
        self.license_plate = license_plate
        self.date_of_purchase = date_of_purchase
        self.status = status
        self.state_of_charge = state_of_charge
        self.electric_capacity = electric_capacity
        self.seat_capacity = seat_capacity


    #  delet the current station object to the database
    def delete_from_database(self):
        conn = self.db_manager.connect()
        cur = conn.cursor()
        # Delete the station record where the number matches
        cur.execute("DELETE FROM buses WHERE number = ?", (self.number,))
        conn.commit()
        print(f"Bus '{self.number}' deleted from database.")


    # Edit any station attribute dynamically
    def EditBus(self, param, value):    
        conn = self.db_manager.connect()
        if hasattr(self, param):
            setattr(self, param, value)
        cur = conn.cursor()
        cur.execute(
            f"UPDATE bus SET {param} = ? WHERE number = ?",
            (value, self.number)
        )
        conn.commit()
        print(f"Bus '{self.number}' updated: {param} = {value}")


    # save the current bus object to the database
    def save_to_database(self):
        conn = self.db_manager.connect()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO buses (license_plate, date_of_purchase, status, state_of_charge, electric_capacity, seat_capacity) VALUES (?, ?, ?, ?, ?, ?)",
            (self.number, self.status, self.state_of_charge, self.electric_capacity)
        )
        conn.commit()
        print(f"bus '{self.number}' saved to database.")

    # Fetch a bus by parameter
    def fetch_station_through_params(self, param, value):
        conn = self.db_manager.connect()
        cur = conn.cursor()
        query = f"SELECT * FROM buses WHERE {param} = ?"
        cur.execute(query, (value,))
        rows = cur.fetchall()
        if rows:
            print("Found:")
            for row in rows:
                print(row)
        else:
            print(f"No bus found with {param} = {value}.")


    
    
