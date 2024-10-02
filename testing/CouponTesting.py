import requests

BASE_URL = "http://127.0.0.1:8000/coupon"

test_restaurant_id = 1
test_coupon_id = 1
test_code = "TESTCODE123"
def test_add_coupon():
    url = f"{BASE_URL}/addCoupon"
    data = {
        "restaurant_id": test_restaurant_id,
        "discount_type": "percentage",
        "discount": 10,
        "description": "Test coupon"
    }
    response = requests.post(url, json=data)
    print("Add Coupon Response:", response.json())

def test_get_coupon_by_id():
    url = f"{BASE_URL}/{test_coupon_id}"
    response = requests.get(url)
    print("Get Coupon by ID Response:", response.json())

def test_get_coupons_by_restaurant_id():
    url = f"{BASE_URL}/couponByRestaurantId/{test_restaurant_id}"
    response = requests.get(url)
    print("Get Coupons by Restaurant ID Response:", response.json())

def test_redeem_coupon():
    url = f"{BASE_URL}/redeem/{test_code}"
    response = requests.get(url)
    print("Redeem Coupon Response:", response.json())

if __name__ == "__main__":
    test_add_coupon()
    test_get_coupon_by_id()
    test_get_coupons_by_restaurant_id()
    test_redeem_coupon()
