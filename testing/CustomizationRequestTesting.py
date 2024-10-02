# testing_customization_request.py
import requests
import json
import logging

base_url = 'http://127.0.0.1:8000/customrequest'

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_add_customization_request():
    url = f'{base_url}/add_customization_request'
    data = {
        "details": "Test customization details",
        "restaurant_user_id": 1  # replace with actual restaurant user ID
    }
    logger.info(f"Sending add customization request: {data}")
    response = requests.post(url, data=json.dumps(data))
    logger.info(f"Received add customization request response: {response.json()}")
    print(response.json())

def test_get_customization_request():
    request_id = 1  # replace with actual request ID
    url = f'{base_url}/customization_request/{request_id}'
    logger.info(f"Sending get customization request for request_id: {request_id}")
    response = requests.get(url)
    logger.info(f"Received get customization request response: {response.json()}")
    print(response.json())

test_add_customization_request()
test_get_customization_request()
