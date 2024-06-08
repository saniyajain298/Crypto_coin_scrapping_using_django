from celery.result import AsyncResult
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView
)
from rest_framework.response import Response
from Crypto_currency_scrapping.celery import scrape_coin_data
from utilities.data_scrapping import scrape_data


# Create your views here.
class StartScrapingAPIView(CreateAPIView):

    def post(self, request, *args, **kwargs):
        coins = request.data["coins"]
        job_id = scrape_coin_data.delay(coins)
        print(job_id)
        response_format = {
            "job_id": str(job_id)
        }
        return Response(response_format, status=status.HTTP_200_OK)


class StatusScrapingAPIView(CreateAPIView):

    def get(self, request, *args, **kwargs):
        job_id = kwargs.get('job_id')
        try:
            result = AsyncResult(job_id)
            print(result.ready())
            response_data = {
                'job_id': result.id,
                'status': result.status,
                'result': result.result if result.successful() else None,
                'traceback': result.traceback if result.failed() else None
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except:
            print("error")
