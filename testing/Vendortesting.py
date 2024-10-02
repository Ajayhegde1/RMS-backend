# vendorTesting.py

import requests
import logging

base_url = 'http://127.0.0.1:8000/vendor'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_register_vendor():
    url = f'{base_url}/register'
    data = {
        "email": "test_vendor@example.com",
        "password": "yourpassword",
        "phone_number": "1234567890",
        "role": "admin"
    }
    logger.info(f"Sending register vendor request: {data}")
    response = requests.post(url, json=data)
    logger.info(f"Received register vendor response: {response.json()}")
    print(response.json())

def test_login():
    url = f'{base_url}/login'
    data = {
        "email": "test_vendor@example.com",
        "password": "yourpassword"
    }
    logger.info(f"Sending login request: {data}")
    response = requests.post(url, json=data)
    logger.info(f"Received login response: {response.json()}")
    print(response.json())
    return response.json()  # Return response to get the access token for other tests

def test_get_vendor_by_id(access_token):
    vendor_id = 1  # replace with actual vendor ID
    url = f'{base_url}/{vendor_id}'
    headers = {"Authorization": f"Bearer {access_token}"}
    logger.info(f"Sending get vendor by ID request for vendor ID: {vendor_id}")
    response = requests.get(url, headers=headers)
    logger.info(f"Received get vendor by ID response: {response.json()}")
    print(response.json())

if __name__ == "__main__":
    test_register_vendor()
    login_response = test_login()
    access_token = login_response.get("access_token")
    if access_token:
        test_get_vendor_by_id(access_token)
    else:
        logger.error("Login failed, no access token obtained")
