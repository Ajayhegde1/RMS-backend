# app/services/cartService.py
from sqlalchemy.orm import Session
from ..models.Cart import Cart as CartModel
from ..models.RestaurantUser import RestaurantUser as RestaurantUserModel
from ..models.NFCDesign import NFCDesign as NFCDesignModel

class CartService:
    @staticmethod
    def add_to_cart(db: Session, user_id: int, nfc_design_id: int):
        # Check if the user exists
        user = db.query(RestaurantUserModel).filter(RestaurantUserModel.id == user_id).first()
        if not user:
            return {"status": "error", "message": "User not found"}
        
        # Check if the NFC design exists
        nfc_design = db.query(NFCDesignModel).filter(NFCDesignModel.id == nfc_design_id).first()
        if not nfc_design:
            return {"status": "error", "message": "NFC design not found"}

        # Check if the item is already in the cart
        cart_item = db.query(CartModel).filter(CartModel.restaurant_user_id == user_id, CartModel.nfc_design_id == nfc_design_id).first()
        if cart_item:
            cart_item.active = True
        else:
            cart_item = CartModel(restaurant_user_id=user_id, nfc_design_id=nfc_design_id, active=True)
            db.add(cart_item)
        
        db.commit()
        db.refresh(cart_item)
        return {"status": "success", "message": "Item added to cart"}

    @staticmethod
    def remove_from_cart(db: Session, user_id: int, nfc_design_id: int):
        # Check if the user exists
        user = db.query(RestaurantUserModel).filter(RestaurantUserModel.id == user_id).first()
        if not user:
            return {"status": "error", "message": "User not found"}
        
        # Check if the NFC design exists
        nfc_design = db.query(NFCDesignModel).filter(NFCDesignModel.id == nfc_design_id).first()
        if not nfc_design:
            return {"status": "error", "message": "NFC design not found"}

        # Check if the item is in the cart
        cart_item = db.query(CartModel).filter(CartModel.restaurant_user_id == user_id, CartModel.nfc_design_id == nfc_design_id).first()
        if cart_item:
            cart_item.active = False
            db.commit()
            db.refresh(cart_item)
            return {"status": "success", "message": "Item removed from cart"}
        else:
            return {"status": "error", "message": "Item not in cart"}

    @staticmethod
    def get_active_items_by_user_id(db: Session, user_id: int):
        return db.query(CartModel).join(NFCDesignModel).filter(CartModel.restaurant_user_id == user_id, CartModel.active == True).all()
