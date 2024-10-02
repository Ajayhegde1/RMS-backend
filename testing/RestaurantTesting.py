import requests
import json
import logging

base_url = 'http://127.0.0.1:8000/restaurant'

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_add_restaurant():
    url = f'{base_url}/add_restaurant'
    data = {
        "name": "Test Restaurant",
        "restaurant_user_id": 1
    }
    logger.info(f"Sending add restaurant request: {data}")
    response = requests.post(url, json=data)
    logger.info(f"Received add restaurant response: {response.json()}")
    print(response.json())

def test_add_restaurant_with_optional_fields():
    url = f'{base_url}/add_restaurant'
    data = {
        "name": "Test Restaurant",
        "branches": ["Branch 1", "Branch 2"],
        "primary_number": "1234567890",
        "secondary_number": "0987654321",
        "restaurant_user_id": 1,  # Replace with actual user ID
        "logo_svg": "<svg>...</svg>",
        "cover_photo_svg": "<svg>...</svg>"
    }
    logger.info(f"Sending add restaurant request with optional fields: {data}")
    response = requests.post(url, json=data)
    logger.info(f"Received add restaurant response with optional fields: {response.json()}")
    print(response.json())

def test_get_restaurant():
    restaurant_id = 1
    url = f'{base_url}/restaurant/{restaurant_id}'
    headers = {"Authorization": "Bearer YOUR_JWT_TOKEN"}  # Replace with actual JWT token
    logger.info(f"Sending get restaurant request for ID: {restaurant_id}")
    response = requests.get(url, headers=headers)
    logger.info(f"Received get restaurant response: {response.json()}")
    print(response.json())

def run_tests():
    test_add_restaurant()
    test_add_restaurant_with_optional_fields()
    test_get_restaurant()

run_tests()
