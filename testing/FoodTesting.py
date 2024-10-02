import requests
import logging

base_url = 'http://127.0.0.1:8000/food'

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_response(response, description):
    logger.info(description)
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response JSON: {response.json()}")

def test_add_food_item_with_all_fields():
    url = f'{base_url}/addFoodItem'
    data = {
        "name": "Test Food 1",
        "category": "Main Course",
        "is_veg": True,
        "cuisine": "Italian",
        "description": "Delicious test food",
        "rating": 4.5,
        "nutritional_value": "High",
        "price": 10.0,
        "image": "image_data",
        "steps": "Step by step preparation",
        "restaurant_id": 1
    }
    response = requests.post(url, json=data)
    log_response(response, "Testing add food item with all fields")

def test_add_food_item_without_optional_fields():
    url = f'{base_url}/addFoodItem'
    data = {
        "name": "Test Food Without Optional 1",
        "restaurant_id": 1,
        "category": "Main Course",
        "is_veg": True,
        "cuisine": "Italian",
        "price": 10.0,
        "steps": "Step by step preparation"
    }
    response = requests.post(url, json=data)
    log_response(response, "Testing add food item without optional fields")

def test_add_raw_material_to_food(food_id, raw_material_id, quantity):
    url = f'{base_url}/addRawMaterialForFood'
    data = {
        "food_id": food_id,
        "raw_material_id": raw_material_id,
        "quantity": quantity
    }
    response = requests.post(url, json=data)
    log_response(response, f"Testing add raw material to food with food_id={food_id} and raw_material_id={raw_material_id}")

def test_get_food_by_id(food_id):
    url = f'{base_url}/getFoodById/{food_id}'
    response = requests.get(url)
    log_response(response, f"Testing get food by ID for food_id={food_id}")

def test_get_all_food_items_by_restaurant(restaurant_id):
    url = f'{base_url}/getAllFoodItemsByRestaurant/{restaurant_id}'
    response = requests.get(url)
    log_response(response, f"Testing get all food items by restaurant for restaurant_id={restaurant_id}")

def test_edit_food(food_id):
    url = f'{base_url}/editFood/{food_id}'
    data = {
        "name": "Updated Test Food 1",
        "category": "Main Course",
        "is_veg": False,
        "cuisine": "Mexican",
        "description": "Updated delicious test food",
        "rating": 4.8,
        "nutritional_value": "Very High",
        "price": 12.0,
        "image": "updated_image_data",
        "steps": "Updated step by step preparation",
        "raw_material": 1
    }
    response = requests.put(url, json=data)
    log_response(response, f"Testing edit food for food_id={food_id}")

def test_delete_food(food_id):
    url = f'{base_url}/deleteFood/{food_id}'
    response = requests.delete(url)
    log_response(response, f"Testing delete food for food_id={food_id}")

if __name__ == "__main__":
    # Replace placeholders with actual IDs and data
    food_id = 1
    raw_material_id = 1
    quantity = 2.0
    restaurant_id = 1

    test_add_food_item_with_all_fields()
    test_add_food_item_without_optional_fields()
    test_add_raw_material_to_food(food_id, raw_material_id, quantity)
    test_get_food_by_id(food_id)
    test_get_all_food_items_by_restaurant(restaurant_id)
    test_edit_food(food_id)
    test_delete_food(food_id)
