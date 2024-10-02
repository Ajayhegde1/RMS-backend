# customerTesting.py

import requests
import logging

base_url = 'http://127.0.0.1:8000/customer'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_add_customer():
    url = f'{base_url}/addCustomer'
    data = {
        "email": "test_customer5@example.com",
        "password": "yourpassword",
        "age": 30,
        "dob": "1993-01-01",
        "phone_number": "1234567890"
    }
    logger.info(f"Sending add customer request: {data}")
    response = requests.post(url, json=data)
    logger.info(f"Received add customer response: {response.json()}")
    print(response.json())

def test_login():
    url = f'{base_url}/login'
    data = {
        "email": "test_customer@example.com",
        "password": "yourpassword"
    }
    logger.info(f"Sending login request: {data}")
    response = requests.post(url, json=data)
    logger.info(f"Received login response: {response.json()}")
    print(response.json())
    return response.json()

def test_get_customer_by_id(access_token):
    customer_id = 1
    url = f'{base_url}/{customer_id}'
    headers = {"Authorization": f"Bearer {access_token}"}
    logger.info(f"Sending get customer by ID request for customer ID: {customer_id}")
    response = requests.get(url, headers=headers)
    logger.info(f"Received get customer by ID response: {response.json()}")
    print(response.json())

if __name__ == "__main__":
    test_add_customer()
    login_response = test_login()
    access_token = login_response.get("access_token")
    if access_token:
        test_get_customer_by_id(access_token)
    else:
        logger.error("Login failed, no access token obtained")

