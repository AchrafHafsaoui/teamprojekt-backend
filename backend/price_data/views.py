import logging
from django.http import JsonResponse
from .entsoe_api import EntsoeDataFetcher

logger = logging.getLogger(__name__)  # Django logging

def get_entsoe_data(request):
    fetcher = EntsoeDataFetcher()
    country_code = 'DE_LU'

    try:
        logger.info("Fetching electricity prices...")  # Log action
        prices = fetcher.get_day_ahead_prices(country_code)
        logger.info(f"Fetched Data: {prices}")  # Log data

        return JsonResponse({"prices": prices}, json_dumps_params={"indent": 2})
    
    except Exception as e:
        logger.error(f"Error fetching ENTSO-E data: {e}")  # Log error
        return JsonResponse({"error": "Failed to fetch data from ENTSO-E", "details": str(e)}, status=500)
