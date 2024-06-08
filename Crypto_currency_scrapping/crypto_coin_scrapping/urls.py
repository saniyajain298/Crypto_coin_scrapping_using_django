from django.urls import path

from .views import StartScrapingAPIView, StatusScrapingAPIView

urlpatterns = [
    path('start_scraping', StartScrapingAPIView.as_view(), name="start_scraping"),
    path('scraping_status/<str:job_id>', StatusScrapingAPIView.as_view(), name="start_status"),
]
