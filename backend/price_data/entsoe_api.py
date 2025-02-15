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
        start = pd.Timestamp(self.start_date, tz='Europe/Brussels')
        end = pd.Timestamp(self.end_date, tz='Europe/Brussels')
        df=self.client.query_day_ahead_prices(country_code, start=start, end=end)
        prices_dict = {str(timestamp): price for timestamp, price in df.items()} 
        return prices_dict


# Usage
if __name__ == "__main__":
    fetcher = EntsoeDataFetcher()
    country_code = 'DE_LU'
    prices = fetcher.get_day_ahead_prices(country_code)
    print(prices)
