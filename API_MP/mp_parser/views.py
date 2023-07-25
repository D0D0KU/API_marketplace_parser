from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import DataSerializer
from .parsers import wb, yandex_market


class ParseDataView(APIView):
    def post(self, request, format=None):
        serializer = DataSerializer(data=request.data)
        if serializer.is_valid():
            # Получаем данные для парсинга из сериализатора
            data_to_parse = serializer.validated_data['data_to_parse']
            
            # Здесь выполните парсинг данных и получите спаршенные данные
            parsed_data = {}
            parsed_data['wb'] = wb.parse_products(data_to_parse, parse_page=1)
            parsed_data['yandex_market'] = yandex_market.parse_products(data_to_parse, parse_page=1)
            
            # Возвращаем спаршенные данные в ответе API
            return Response({'parsed_data': parsed_data})
        return Response(serializer.errors, status=400)

