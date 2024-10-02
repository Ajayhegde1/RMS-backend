# main.py
from fastapi import FastAPI
from .database import create_tables
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()


# app.mount("/_next", StaticFiles(directory="/var/www/frontEndRMS/frontEnd/.next"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)


@app.on_event("startup")
async def startup_event():
    create_tables()

from .controllers import VendorController, CustomerController, CouponController, FoodRecipeStepsController
from .controllers import BaseDesignController, CustomizationRequestController, FoodController
from .controllers import RestaurantUserController, RestaurantController, GenerateQrController,ReviewController
from .controllers import CuisineController, NFCDesignController, CartController, RawMaterialController


app.include_router(VendorController.router, prefix="/api/vendor")
app.include_router(ReviewController.router, prefix="/api/review")
app.include_router(BaseDesignController.router, prefix="/api/vendor_base_design")
app.include_router(RestaurantUserController.router, prefix="/api/restaurantUser")
app.include_router(RestaurantController.router, prefix="/api/restaurant")
app.include_router(CustomizationRequestController.router, prefix="/api/customrequest")
app.include_router(GenerateQrController.router, prefix="/api/qrs")
app.include_router(CuisineController.router, prefix="/api/cuisine")
app.include_router(NFCDesignController.router, prefix="/api/nfcdesign")
app.include_router(CartController.router, prefix="/api/cart")
app.include_router(CustomerController.router, prefix="/api/customer")
app.include_router(CouponController.router, prefix="/api/coupon")
app.include_router(RawMaterialController.router, prefix="/api/rawMaterial")
app.include_router(FoodController.router, prefix="/api/food")
app.include_router(FoodRecipeStepsController.router, prefix="/api/foodRecipeSteps")

@app.get("/api/")
async def root():
    return {"message": "Hello World"}
