import requests
import logging

base_url = 'http://127.0.0.1:8000/rawMaterial'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_create_raw_material():
    url = f'{base_url}/addRawMaterial'
    data = {
        "name": "Tomatos",
        "quantity": 100,
        "price": 1.5,
        "category": "Vegetables",
        "unit": "kg",
        "restaurant_id": 1  # Example restaurant ID, replace with actual value
    }
    logger.info(f"Sending create raw material request: {data}")
    response = requests.post(url, json=data)
    logger.info(f"Received create raw material response: {response.json()}")
    print(response.json())

def test_get_all_raw_materials():
    url = f'{base_url}/getAllRawMaterials'
    logger.info("Sending get all raw materials request")
    response = requests.get(url)
    logger.info(f"Received get all raw materials response: {response.json()}")
    print(response.json())

def test_get_raw_material_by_id():
    raw_material_id = 1  # replace with actual raw material ID
    url = f'{base_url}/getRawMaterialById/{raw_material_id}'
    logger.info(f"Sending get raw material by ID request for ID: {raw_material_id}")
    response = requests.get(url)
    logger.info(f"Received get raw material by ID response: {response.json()}")
    print(response.json())

def test_get_raw_material_by_name():
    name = "Tomato"  # replace with actual name to search
    restaurant_id = 1  # replace with actual restaurant ID
    url = f'{base_url}/getRawMaterialByName/search/{name}?restaurant_id={restaurant_id}'
    logger.info(f"Sending get raw material by name request for name: {name} and restaurant_id: {restaurant_id}")
    response = requests.get(url)
    logger.info(f"Received get raw material by name response: {response.json()}")
    print(response.json())

def test_get_all_raw_materials_by_restaurant():
    restaurant_id = 1  # replace with actual restaurant ID
    url = f'{base_url}/getAllRawMaterialsByRestaurant?restaurant_id={restaurant_id}'
    logger.info(f"Sending get all raw materials by restaurant request for restaurant ID: {restaurant_id}")
    response = requests.get(url)
    logger.info(f"Received get all raw materials by restaurant response: {response.json()}")
    print(response.json())

if __name__ == "__main__":
    test_create_raw_material()
    test_get_all_raw_materials()
    test_get_raw_material_by_id()
    test_get_raw_material_by_name()
    test_get_all_raw_materials_by_restaurant()
