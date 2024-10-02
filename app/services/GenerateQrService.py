# app/services/GenerateQrService.py
import io
from sqlalchemy.orm import Session
from ..models.GenerateQR import GenerateQR as GenerateQrModel
from ..models.Platform import Platform as PlatformModel

class GenerateQrService:
    @staticmethod
    def generate_qr_svg(data: str) -> str:
        # factory = qrcode.image.svg.SvgImage
        # qr = qrcode.make(data, image_factory=factory)
        stream = io.BytesIO()
        # qr.save(stream)
        stream.seek(0)
        return stream.getvalue()

    @staticmethod
    def add_platform_if_not_exists(db: Session, platform_name: str):
        platform = db.query(PlatformModel).filter(PlatformModel.name == platform_name).first()
        if not platform:
            new_platform = PlatformModel(name=platform_name)
            db.add(new_platform)
            db.commit()
            db.refresh(new_platform)
            return new_platform
        return platform

    @staticmethod
    def create_qr(db: Session, qr_data: GenerateQrModel):
        db.add(qr_data)
        db.commit()
        db.refresh(qr_data)
        return qr_data

    @staticmethod
    def get_qrs_by_user_id(db: Session, user_id: int):
        return db.query(GenerateQrModel).filter(GenerateQrModel.restaurant_user_id == user_id, GenerateQrModel.active == True).all()
    
    @staticmethod
    def get_qr_by_id(db: Session, qr_id: int):
        return db.query(GenerateQrModel).filter(GenerateQrModel.id == qr_id, GenerateQrModel.active == True).first()
    
    @staticmethod
    def update_qr(db: Session, qr_id: int, update_data: dict):
        qr = db.query(GenerateQrModel).filter(GenerateQrModel.id == qr_id, GenerateQrModel.active == True).first()
        if not qr:
            return None
        for key, value in update_data.items():
            setattr(qr, key, value)
        db.commit()
        db.refresh(qr)
        return qr

    @staticmethod
    def delete_qr(db: Session, qr_id: int):
        qr = db.query(GenerateQrModel).filter(GenerateQrModel.id == qr_id, GenerateQrModel.active == True).first()
        if qr:
            qr.active = False
            db.commit()
        return qr
