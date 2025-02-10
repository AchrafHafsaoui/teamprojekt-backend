from django.http import JsonResponse
from .entsoe_api import EntsoeDataFetcher  # Import your class

def get_entsoe_data(request):
    fetcher = EntsoeDataFetcher()
    country_code = 'DE_LU'  # You can modify this to accept user input
    try:
        prices = fetcher.get_day_ahead_prices(country_code)
        return JsonResponse(prices.to_dict(), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
