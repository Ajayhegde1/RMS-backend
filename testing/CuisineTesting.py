# testing_cuisine.py
import requests
import json
import logging

base_url = 'http://127.0.0.1:8000/cuisine'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_add_cuisine():
    url = f'{base_url}/addCuisine'
    data = {
        "name": "Italian",
        "cuisine_image_svg": "<svg>...</svg>",
        "base_design_id": 1
    }
    logger.info(f"Sending add cuisine request: {data}")
    response = requests.post(url, data=json.dumps(data))
    logger.info(f"Received add cuisine response: {response.json()}")
    print(response.json())

def test_get_cuisines_by_base_design():
    base_design_id = 1 
    url = f'{base_url}/cuisines/{base_design_id}'
    logger.info(f"Fetching cuisines for base_design_id: {base_design_id}")
    response = requests.get(url)
    logger.info(f"Received cuisines: {response.json()}")
    print(response.json())

if __name__ == "__main__":
    test_add_cuisine()
    test_get_cuisines_by_base_design()
