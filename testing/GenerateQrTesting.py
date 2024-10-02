# testing_generate_qr.py
import requests
import json
import logging

base_url = 'http://127.0.0.1:8000/qrs'

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_generate_qr():
    url = f'{base_url}/generateQr'
    data = {
        "restaurant_user_id": 1,
        "orientation": "horizontal",
        "review_page_link": "http://google.com",
        "platform_name": "Yelp"
    }
    logger.info(f"Sending generate QR request: {data}")
    #response = requests.post(url, data=json.dumps(data))
    response = requests.post(url, json=data)

    logger.info(f"Received generate QR response: {response.json()}")
    print(response.json())

def test_get_qrs_by_user():
    restaurant_user_id = 1
    url = f'{base_url}/qrs_by_user/{restaurant_user_id}'
    logger.info(f"Fetching QR codes for restaurant_user_id: {restaurant_user_id}")
    response = requests.get(url)
    logger.info(f"Received QR codes: {response.json()}")
    print(response.json())

if __name__ == "__main__":
    test_generate_qr()
    test_get_qrs_by_user()
