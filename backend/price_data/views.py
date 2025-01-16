from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .entsoe_api import EntsoeDataFetcher


class EntsoeDataView(APIView):
    def get(self, request):
        fetcher = EntsoeDataFetcher()
        country_code = 'DE_LU' 
        try:
            prices = fetcher.get_day_ahead_prices(country_code)
            return Response(prices.to_dict(), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



