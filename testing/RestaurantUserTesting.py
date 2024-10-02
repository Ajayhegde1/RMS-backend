# testingRestaurantUser.py
import requests
import json
import logging

base_url = 'http://127.0.0.1:8000/restaurantUser'

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_restaurant_signup():
    url = f'{base_url}/restaurant_signup'
    data = {
        "email": "testrestaurantuser@example.com",
        "password": "testpassword",
        "phone_number": "1234567890"
    }
    logger.info(f"Sending restaurant signup request: {data}")
    response = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    logger.info(f"Received restaurant signup response: {response.json()}")
    print(response.json())

def test_restaurant_login():
    url = f'{base_url}/restaurant_login'
    data = {
        "email": "testrestaurantuser@example.com",
        "password": "testpassword"
    }
    logger.info(f"Sending restaurant login request: {data}")
    response = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    logger.info(f"Received restaurant login response: {response.json()}")
    print(response.json())
    return response.json().get("access_token")

def test_view_profile(access_token):
    user_id = 1
    url = f'{base_url}/restaurant_user_profile/{user_id}'
    headers = {"Authorization": f"Bearer {access_token}"}
    logger.info(f"Sending restaurant user profile view request for user_id: {user_id}")
    response = requests.get(url, headers=headers)
    logger.info(f"Received restaurant user profile view response: {response.json()}")
    print(response.json())

def run_tests():
    test_restaurant_signup()
    access_token = test_restaurant_login()
    if access_token:
        test_view_profile(access_token)

run_tests()
