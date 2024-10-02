# app/controllers/BaseDesignController.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..models.BaseDesign import BaseDesign as BaseDesignModel
from ..models.Cuisine import Cuisine as CuisineModel
from ..services.BaseDesignService import BaseDesignService
from ..services.VendorService import VendorService
from ..database import get_db

import logging

router = APIRouter()

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/base_design")
async def create_base_design(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    logger.info(f"Received base design request: {data}")

    base_design_front_svg = data.get("base_design_front_svg")
    base_design_back_svg = data.get("base_design_back_svg")
    base_design_svg = data.get("base_design_svg")
    price = data.get("price")
    vendor_id = data.get("vendor_id")

    if not all([base_design_front_svg, base_design_back_svg, base_design_svg, price, vendor_id]):
        logger.warning("Required fields not provided in request")
        raise HTTPException(status_code=400, detail="All base design fields and vendor ID are required")

    if VendorService.get_vendor_by_id(db, vendor_id) is None:
        raise HTTPException(status_code=400, detail="Vendor not found")

    base_design = BaseDesignModel(
        base_design_front_svg=base_design_front_svg,
        base_design_back_svg=base_design_back_svg,
        base_design_svg=base_design_svg,
        price=price,
        vendor_id=vendor_id
    )
    db_base_design = BaseDesignService.create_base_design(db=db, base_design=base_design)
    logger.info(f"Base design created successfully with ID: {db_base_design.id}")

    return {"statusCode": 200, "detail": "Base design added successfully", "response": db_base_design}

@router.post("/base_design_with_cuisine")
async def create_base_design_with_cuisine(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    logger.info(f"Received base design with cuisine request: {data}")

    base_design_front_svg = data.get("base_design_front_svg")
    base_design_back_svg = data.get("base_design_back_svg")
    base_design_svg = data.get("base_design_svg")
    price = data.get("price")
    vendor_id = data.get("vendor_id")
    cuisine_name = data.get("cuisine_name")
    cuisine_image_svg = data.get("cuisine_image_svg")

    if not all([base_design_front_svg, base_design_back_svg, base_design_svg, price, vendor_id, cuisine_name, cuisine_image_svg]):
        logger.warning("Required data not provided in request")
        raise HTTPException(status_code=400, detail="All base design fields, vendor ID, cuisine name, and cuisine image SVG are required")

    if VendorService.get_vendor_by_id(db, vendor_id) is None:
        raise HTTPException(status_code=400, detail="Vendor not found")

    base_design = BaseDesignModel(
        base_design_front_svg=base_design_front_svg,
        base_design_back_svg=base_design_back_svg,
        base_design_svg=base_design_svg,
        price=price,
        vendor_id=vendor_id
    )
    db_base_design = BaseDesignService.create_base_design(db=db, base_design=base_design)

    cuisine = CuisineModel(
        name=cuisine_name,
        cuisine_image_svg=cuisine_image_svg,
        base_design_id=db_base_design.id
    )
    db_cuisine = BaseDesignService.create_cuisine(db=db, cuisine=cuisine)
    logger.info(f"Cuisine created successfully with ID: {db_cuisine.id}")

    return {"statusCode": 200, "detail": "Base design and cuisine added successfully", "response": {"base_design": db_base_design, "cuisine": db_cuisine}}

@router.get("/base_design/{vendor_id}")
async def get_base_designs(vendor_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching base designs for vendor ID: {vendor_id}")

    if VendorService.get_vendor_by_id(db, vendor_id) is None:
        raise HTTPException(status_code=400, detail="Vendor not found")

    base_designs = BaseDesignService.get_base_designs_by_vendor_id(db, vendor_id=vendor_id)
    if not base_designs:
        logger.warning(f"No base designs found for vendor ID: {vendor_id}")
        raise HTTPException(status_code=404, detail="No base designs found")

    logger.info(f"Base designs fetched for vendor ID: {vendor_id}")
    return {"statusCode": 200, "detail": "Base designs fetched successfully", "response": base_designs}

@router.put("/base_design/{base_design_id}")
async def update_base_design(base_design_id: int, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    logger.info(f"Received update base design request: {data}")

    updated_base_design = BaseDesignService.update_base_design(db=db, base_design_id=base_design_id, base_design_data=data)
    if not updated_base_design:
        logger.warning(f"Base design with ID {base_design_id} not found or inactive")
        raise HTTPException(status_code=404, detail="Base design not found")

    logger.info(f"Base design ID {base_design_id} updated successfully")
    return {"statusCode": 200, "detail": "Base design updated successfully", "response": updated_base_design}

@router.delete("/base_design/{base_design_id}")
async def delete_base_design(base_design_id: int, db: Session = Depends(get_db)):
    logger.info(f"Received delete base design request for base_design_id: {base_design_id}")

    deleted_base_design = BaseDesignService.delete_base_design(db=db, base_design_id=base_design_id)
    if not deleted_base_design:
        logger.warning(f"Base design with ID {base_design_id} not found or inactive")
        raise HTTPException(status_code=404, detail="Base design not found")

    logger.info(f"Base design ID {base_design_id} marked as inactive")
    return {"statusCode": 200, "detail": "Base design deleted successfully (soft delete)", "response": deleted_base_design}


