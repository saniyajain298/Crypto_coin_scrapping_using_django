import os

from celery import Celery

from utilities.data_scrapping import scrape_data

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Crypto_currency_scrapping.settings')

app = Celery('Crypto_currency_scrapping')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
@app.task
def scrape_coin_data(coins):
    response_format = []
    for coin in coins:
        output = scrape_data(coin)
        if isinstance(output, str):
            print("iniside if")
            output = scrape_data(coin)

        print("output", output)
        response_format.append({
            "coin": coin,
            "output": output
        })
    return response_format
