#app/services/CustomizationRequestService.py
from sqlalchemy.orm import Session
from ..models.CustomizationRequest import CustomizationRequest as CustomizationRequestModel

class CustomizationRequestService:
    @staticmethod
    def create_customization_request(db: Session, customization_request: CustomizationRequestModel):
        db.add(customization_request)
        db.commit()
        db.refresh(customization_request)
        return customization_request

    @staticmethod
    def get_customization_request_by_id(db: Session, request_id: int):
        return db.query(CustomizationRequestModel).filter(CustomizationRequestModel.id == request_id).first()
