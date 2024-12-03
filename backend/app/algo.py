import polars as pl
from datetime import datetime, timedelta


# Preconditioning and it's period will be chosen by the admin
preconditioning = True
preconditioning_period = 30
file_paths = "arrivalDepartureDummy.parquet"
# placeholders
datetimenow = "2024-12-02 16:07:14"
datetimenow_dt = datetime.strptime(datetimenow, "%Y-%m-%d %H:%M:%S")


class FleetManager:

    def __init__(self, file_path = file_paths, preconditioning_time = preconditioning_period):
        """
        Constructor for the FleetManager class.

        Args:
            file_path (str): Path to the Parquet file containing fleet data.
            preconditioning_time (int): Time in minutes to subtract for preconditioning.
        """
        self.file_path = file_path
        self.preconditioning_time = preconditioning_time

    def fetch_24h_departures(self):
        """
        Fetch departures scheduled for the next 24 hours.

        Reads data from a Parquet file, filters for "departure" events, and processes
        event times to ensure they are within the next 24 hours from the current time.

        Returns:
            DataFrame: A DataFrame with filtered departures and renamed 'event_time' column to 'departure_time'.
        """
        departures = pl.scan_parquet(self.file_path)
        departures = departures.filter(pl.col("event_type") == "departure").collect()
        next_24_hours = datetimenow_dt + timedelta(days=1) # TODO:change datetimenoew to datetime.now()
        departures = departures.filter(pl.col("event_time").str.strptime(pl.Datetime, format="%Y-%m-%d %H:%M:%S") <= pl.lit(next_24_hours))
        departures = departures.rename({"event_time": "departure_time"})
        
        return departures
    
    def fetch_24h_arrivals(self):
        """
        Fetch arrivals scheduled for the next 24 hours.

        Reads data from a Parquet file, filters for "arrival" events, and processes
        event times to ensure they are within the next 24 hours from the current time.

        Returns:
            DataFrame: A DataFrame with filtered arrivals and renamed 'event_time' column to 'arrival_time'.
        """
        arrivals = pl.scan_parquet(self.file_path)
        arrivals = arrivals.filter(pl.col("event_type") == "arrival").collect()
        next_24_hours = datetimenow_dt + timedelta(days=1) # TODO:change datetimenoew to datetime.now()
        arrivals = arrivals.filter(pl.col("event_time").str.strptime(pl.Datetime, format="%Y-%m-%d %H:%M:%S") <= pl.lit(next_24_hours))
        arrivals = arrivals.rename({"event_time": "arrival_time"})
        
        return arrivals
    
    def fetch_dapartures_and_arrivals(self):
        """
        Fetch both departures and arrivals for the next 24 hours.

        Reads data from a Parquet file and filters events based on the event time being
        within the next 24 hours.

        Returns:
            DataFrame: A combined DataFrame of all events within the specified time frame.
        """
        events = pl.scan_parquet(self.file_path).collect()
        next_24_hours = datetimenow_dt + timedelta(days=1) # TODO:change datetimenoew to datetime.now()
        events = events.filter(pl.col("event_time").str.strptime(pl.Datetime, format="%Y-%m-%d %H:%M:%S") <= pl.lit(next_24_hours))
        events = events.with_columns(
            pl.col("event_time").str.strptime(pl.Datetime, format="%Y-%m-%d %H:%M:%S")
        )
        
        return events
        

    def plan_preconditioning(self, preconditioning_period: int):
        """
        Plan preconditioning schedule for departures.

        Adjusts the 'plug_in_at' time for preconditioning and calculates the finish time.
        The preconditioning is scheduled to start a specified number of minutes before departure.

        Args:
            preconditioning_period (int): Time in minutes to subtract for preconditioning.

        Returns:
            DataFrame: A DataFrame with adjusted preconditioning schedule.
        """
        departures = self.fetch_24h_departures()
        planning = departures.rename({
            "departure_time": "plug_in_at", 
        })
        planning = planning.with_columns(
            pl.col("plug_in_at").alias("finish_at"),
            pl.lit("Preconditioning").alias("type")
        )
        planning = planning.with_columns(
            (pl.col("plug_in_at").str.strptime(pl.Datetime, format="%Y-%m-%d %H:%M:%S") - timedelta(minutes=preconditioning_period)).dt.strftime("%Y-%m-%d %H:%M:%S").alias("plug_in_at")
        )

        return planning
    
    
    def plan_charging(self):
        """
        Plan charging schedule for buses.

        This method calculates §b= arrival_time - departure_time - length_of_charging,
        and find the best possible charging interval for a minimun peak load on the grid.

        Returns:
            DataFrame: A DataFrame with matched arrivals and departures, sorted by adjusted charging duration.
        """
        # iterae over every bus that came
                # if bus will leave in the next 24 hours
                    # calculate §b= arrival_time - departure_time - length_of_charging
        arrivals= self.fetch_24h_arrivals()
        departures = self.fetch_24h_departures()
        departures = departures.with_columns(
            pl.col("departure_time").str.strptime(pl.Datetime, format="%Y-%m-%d %H:%M:%S").alias("departure_time")
        )
        arrivals = arrivals.with_columns(
            pl.col("arrival_time").str.strptime(pl.Datetime, format="%Y-%m-%d %H:%M:%S")
        
        )
        cross_joined = arrivals.join(
            departures,
            how="cross",
            suffix="_right"  # To distinguish columns if needed
        )
        matched = cross_joined.filter(
            (pl.col("license_plate") == pl.col("license_plate_right")) & 
            (pl.col("departure_time") > pl.col("arrival_time"))
        )
        matched = matched.select([
            pl.col("arrival_time"),
            pl.col("departure_time"),
            pl.col("license_plate")
        ])

        matched = matched.with_columns(
            (pl.col("departure_time") - pl.col("arrival_time") - timedelta(minutes=self.preconditioning_time)).alias("alphaB")
        )
        # Arrange Buses ascending by §b
        matched = matched.sort("alphaB")

        # for i in arrivals:
        #for i in matched:
        # TODO
        # bus = Buses(i)
            
            # Calculate Pbus

            # Calculate Hmax for all charging intervals in range Pbus (Hmax i peak demand in a certain time)
            
            # Choose Cbus as a tuple of charging intervals from P bus with the least Hmax
            
            # If |Cbus| > 1
            
                    # Redefine Cbus as a tuple of charging intervals from Cbus with the least Hinterval
            
                # If |Cbus| > 1
            
                    # Redefine Cbus as the charging interval from Cbus with the earliest charging start s
        
        # C bus is the chosen charging interva for bus
       
        return matched


     
            
        
        
    
            
            


fleet = FleetManager(file_paths)
departures_sorted = fleet.plan_charging()
print(departures_sorted)
