# "2c87f973-5932-4e2e-a573-1825782df831"


from datetime import datetime, timedelta
from entsoe import EntsoePandasClient
import pandas as pd

class EntsoeDataFetcher:
    def __init__(self):
        self.client = EntsoePandasClient(api_key="2c87f973-5932-4e2e-a573-1825782df831")
        self.start_date = datetime.now().date()
        self.end_date = self.start_date + timedelta(days=1)
        
    def get_day_ahead_prices(self, country_code):
        # Calculate yesterday's date range
        yesterday_start = self.start_date - timedelta(days=1)
        yesterday_end = self.start_date

        # Convert to timestamps with timezone
        start_yesterday = pd.Timestamp(yesterday_start, tz='Europe/Brussels')
        end_yesterday = pd.Timestamp(yesterday_end, tz='Europe/Brussels')

        # Query day-ahead prices for yesterday
        df_yesterday = self.client.query_day_ahead_prices(country_code, start=start_yesterday, end=end_yesterday)

        # Calculate today's date range
        start_today = pd.Timestamp(self.start_date, tz='Europe/Brussels')
        end_today = pd.Timestamp(self.end_date, tz='Europe/Brussels')

        # Query day-ahead prices for today
        df_today = self.client.query_day_ahead_prices(country_code, start=start_today, end=end_today)

        # Convert both results to lists of dictionaries
        prices_yesterday = [{"timestamp": str(timestamp), "price": price} for timestamp, price in df_yesterday.items()]
        prices_today = [{"timestamp": str(timestamp), "price": price} for timestamp, price in df_today.items()]

        # Return the data as a dictionary
        return {
            "yesterday": prices_yesterday,
            "today": prices_today
        }


# Usage
if __name__ == "__main__":
    fetcher = EntsoeDataFetcher()
    country_code = 'DE_LU'  # Example country code for Germany/Luxembourg
    data = fetcher.get_day_ahead_prices(country_code)
    print(data)
