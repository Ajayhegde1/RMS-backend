# BaseDesignTesting.py
import requests
import json
import logging

base_url = 'http://127.0.0.1:8000/vendor_base_design'

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_create_base_design():
    url = f'{base_url}/base_design'
    data = {
        "base_design_front_svg": "<svg>...</svg>",
        "base_design_back_svg": "<svg>...</svg>",
        "base_design_svg": "<svg>...</svg>",
        "price": 100.0,
        "vendor_id": 1
    }
    headers = {'Content-Type': 'application/json'}
    logger.info(f"Sending create base design request: {data}")
    response = requests.post(url, data=json.dumps(data), headers=headers)
    logger.info(f"Received create base design response: {response.json()}")
    print(response.json())

def test_create_base_design_with_cuisine():
    url = f'{base_url}/base_design_with_cuisine'
    data = {
        "base_design_front_svg": "<svg>...</svg>",
        "base_design_back_svg": "<svg>...</svg>",
        "base_design_svg": "<svg>...</svg>",
        "price": 150.0,
        "vendor_id": 1,
        "cuisine_name": "Test Cuisine",
        "cuisine_image_svg": "<svg>...</svg>"
    }
    headers = {'Content-Type': 'application/json'}
    logger.info(f"Sending create base design with cuisine request: {data}")
    response = requests.post(url, data=json.dumps(data), headers=headers)
    logger.info(f"Received create base design with cuisine response: {response.json()}")
    print(response.json())

def test_get_base_designs():
    vendor_id = 1
    url = f'{base_url}/base_design/{vendor_id}'
    logger.info(f"Sending get base designs request for vendor_id: {vendor_id}")
    response = requests.get(url)
    logger.info(f"Received get base designs response: {response.json()}")
    print(response.json())

if __name__ == "__main__":
    test_create_base_design()
    test_create_base_design_with_cuisine()
    test_get_base_designs()
