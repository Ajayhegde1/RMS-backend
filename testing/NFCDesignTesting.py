# NFCDesignTesting.py
import requests
import json
import logging

base_url = 'http://127.0.0.1:8000/nfcdesign'

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_add_nfc_design():
    url = f'{base_url}/addNFCDesign'
    data = {
        "design_name": "Modern",  
        "template_svg": "<svg>...</svg>",
        "total_price": 9.99,
        "generate_qr_id": 1,
        "base_design_id": 1,
        "cuisine_id": 1
    }
    logger.info(f"Sending add NFC design request: {data}")
    response = requests.post(url, data=json.dumps(data))
    logger.info(f"Received add NFC design response: {response.json()}")
    print(response.json())

def test_get_all_nfc_designs():
    url = f'{base_url}/nfcDesigns'
    logger.info("Fetching all NFC designs")
    response = requests.get(url)
    logger.info(f"Received all NFC designs: {response.json()}")
    print(response.json())

def test_get_nfc_designs_by_user():
    restaurant_user_id = 1 
    url = f'{base_url}/nfcDesignsByUser/{restaurant_user_id}'
    logger.info(f"Fetching NFC designs for restaurant_user_id: {restaurant_user_id}")
    response = requests.get(url)
    logger.info(f"Received NFC designs by user: {response.json()}")
    print(response.json())

def test_get_nfc_design():
    nfc_design_id = 1 
    url = f'{base_url}/nfcDesign/{nfc_design_id}'
    logger.info(f"Fetching NFC design for nfc_design_id: {nfc_design_id}")
    response = requests.get(url)
    logger.info(f"Received NFC design: {response.json()}")
    print(response.json())

if __name__ == "__main__":
    test_add_nfc_design()
    test_get_all_nfc_designs()
    test_get_nfc_designs_by_user()
    test_get_nfc_design()
