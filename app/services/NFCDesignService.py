# app/services/NFCDesignService.py
from sqlalchemy.orm import Session
from ..models.NFCDesign import NFCDesign as NFCDesignModel
from ..models.GenerateQR import GenerateQR as GenerateQrModel

class NFCDesignService:
    @staticmethod
    def create_nfc_design(db: Session, nfc_design_data: NFCDesignModel):
        db.add(nfc_design_data)
        db.commit()
        db.refresh(nfc_design_data)
        return nfc_design_data
    
    @staticmethod
    def get_all_nfc_designs(db: Session):
        return db.query(NFCDesignModel).filter(NFCDesignModel.active == True).all()

    @staticmethod
    def get_nfc_designs_by_restaurant_user_id(db: Session, restaurant_user_id: int):
        return db.query(NFCDesignModel).join(GenerateQrModel).filter(GenerateQrModel.restaurant_user_id == restaurant_user_id, NFCDesignModel.active == True).all()
    
    @staticmethod
    def get_nfc_design_by_id(db: Session, nfc_design_id: int):
        return db.query(NFCDesignModel).filter(NFCDesignModel.id == nfc_design_id, NFCDesignModel.active == True).first()

    @staticmethod
    def update_nfc_design(db: Session, nfc_design_id: int, update_data: dict):
        nfc_design = db.query(NFCDesignModel).filter(NFCDesignModel.id == nfc_design_id, NFCDesignModel.active == True).first()
        if not nfc_design:
            return None
        for key, value in update_data.items():
            setattr(nfc_design, key, value)
        db.commit()
        db.refresh(nfc_design)
        return nfc_design

    @staticmethod
    def delete_nfc_design(db: Session, nfc_design_id: int):
        nfc_design = db.query(NFCDesignModel).filter(NFCDesignModel.id == nfc_design_id, NFCDesignModel.active == True).first()
        if nfc_design:
            nfc_design.active = False
            db.commit()
        return nfc_design


