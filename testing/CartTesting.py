import requests

BASE_URL = "http://127.0.0.1:8000/cart"

test_user_id = 1
test_nfc_design_id = 1

def test_add_to_cart():
    url = f"{BASE_URL}/addToCart"
    data = {
        "restaurant_user_id": test_user_id,
        "nfc_design_id": test_nfc_design_id
    }
    response = requests.post(url, json=data)
    print("Add to Cart Response:", response.json())

def test_remove_from_cart():
    url = f"{BASE_URL}/removeFromCart"
    data = {
        "restaurant_user_id": test_user_id,
        "nfc_design_id": test_nfc_design_id
    }
    response = requests.post(url, json=data)
    print("Remove from Cart Response:", response.json())

def test_get_active_items_by_user():
    url = f"{BASE_URL}/activeItems/{test_user_id}"
    response = requests.get(url)
    print("Active Items Response:", response.json())

if __name__ == "__main__":
    test_add_to_cart()
    test_remove_from_cart()
    test_get_active_items_by_user()
