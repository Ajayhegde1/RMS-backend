# app/controllers/NFCDesignController.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..models.NFCDesign import NFCDesign as NFCDesignModel
from ..services.NFCDesignService import NFCDesignService
from ..database import get_db

import logging

router = APIRouter()

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/addNFCDesign")
async def add_nfc_design(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    logger.info(f"Received add NFC design request: {data}")

    design_name = data.get("design_name")
    template_svg = data.get("template_svg")
    total_price = data.get("total_price")
    generate_qr_id = data.get("generate_qr_id")
    base_design_id = data.get("base_design_id")
    cuisine_id = data.get("cuisine_id")

    if not (design_name and template_svg and total_price and generate_qr_id and base_design_id and cuisine_id):
        logger.warning("Missing required fields in add NFC design request")
        raise HTTPException(status_code=400, detail="Missing required fields")

    nfc_design = NFCDesignModel(
        design_name=design_name,
        template_svg=template_svg,
        total_price=total_price,
        generate_qr_id=generate_qr_id,
        base_design_id=base_design_id,
        cuisine_id=cuisine_id
    )

    created_nfc_design = NFCDesignService.create_nfc_design(db=db, nfc_design_data=nfc_design)
    logger.info(f"NFC Design {design_name} created successfully")

    return {"statusCode": 200, "detail": "NFC design added successfully", "response": created_nfc_design}

@router.get("/nfcDesigns")
async def get_all_nfc_designs(db: Session = Depends(get_db)):
    logger.info("Fetching all NFC designs")

    nfc_designs = NFCDesignService.get_all_nfc_designs(db)
    if not nfc_designs:
        logger.warning("No NFC designs found")
        raise HTTPException(status_code=404, detail="No NFC designs found")

    logger.info("NFC designs fetched")
    return {"statusCode": 200, "detail": "NFC designs fetched successfully", "response": nfc_designs}

@router.get("/nfcDesignsByUser/{restaurant_user_id}")
async def get_nfc_designs_by_user(restaurant_user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching NFC designs for restaurant_user_id: {restaurant_user_id}")

    nfc_designs = NFCDesignService.get_nfc_designs_by_restaurant_user_id(db, restaurant_user_id)
    if not nfc_designs:
        logger.warning(f"No NFC designs found for restaurant_user_id: {restaurant_user_id}")
        raise HTTPException(status_code=404, detail="No NFC designs found for this user")

    logger.info(f"NFC designs fetched for restaurant_user_id: {restaurant_user_id}")
    return {"statusCode": 200, "detail": "NFC designs fetched successfully for user", "response": nfc_designs}

@router.get("/nfcDesign/{nfc_design_id}")
async def get_nfc_design(nfc_design_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching NFC design for nfc_design_id: {nfc_design_id}")

    nfc_design = NFCDesignService.get_nfc_design_by_id(db, nfc_design_id)
    if not nfc_design:
        logger.warning(f"NFC design with ID {nfc_design_id} not found")
        raise HTTPException(status_code=404, detail="NFC design not found")

    logger.info(f"NFC design fetched for nfc_design_id: {nfc_design_id}")
    return {"statusCode": 200, "detail": "NFC design fetched successfully", "response": nfc_design}

@router.put("/update_nfcDesign/{nfc_design_id}")
async def update_nfc_design(nfc_design_id: int, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    logger.info(f"Received update request for NFC design ID: {nfc_design_id} with data: {data}")
    
    updated_nfc_design = NFCDesignService.update_nfc_design(db=db, nfc_design_id=nfc_design_id, update_data=data)
    if not updated_nfc_design:
        logger.warning(f"NFC design ID {nfc_design_id} not found or inactive")
        raise HTTPException(status_code=404, detail="NFC design not found")
    
    logger.info(f"NFC design ID {nfc_design_id} updated successfully")
    
    return {
        "statusCode": 200,
        "detail": "NFC design updated successfully",
        "response": updated_nfc_design
    }

@router.delete("/delete_nfcDesign/{nfc_design_id}")
async def delete_nfc_design(nfc_design_id: int, db: Session = Depends(get_db)):
    logger.info(f"Received delete request for NFC design ID: {nfc_design_id}")
    
    deleted_nfc_design = NFCDesignService.delete_nfc_design(db=db, nfc_design_id=nfc_design_id)
    if not deleted_nfc_design:
        logger.warning(f"NFC design ID {nfc_design_id} not found or inactive")
        raise HTTPException(status_code=404, detail="NFC design not found")
    
    logger.info(f"NFC design ID {nfc_design_id} marked as inactive")
    
    return {
        "statusCode": 200,
        "detail": "NFC design deleted successfully (soft delete)",
        "response": deleted_nfc_design
    }

