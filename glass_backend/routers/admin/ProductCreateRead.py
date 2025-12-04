from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database_connector import get_db
from models.ProductModel import (
    AddNewProduct,
    ProductResponse,
)
from database.ProductTable import Product, ProductBenefits, ProductSpecifications, InstallationGallery as ORMGallery
from typing import List
router = APIRouter(prefix="/product", tags=["product"])

# --------------------- CREATE PRODUCT ---------------------
@router.post("/add-product", response_model=ProductResponse)
def add_product(product_data: AddNewProduct, db: Session = Depends(get_db)):
    new_product = Product(
        category=product_data.category,
        product_type=product_data.product_type,
        product_image=product_data.product_image,
        product_name=product_data.product_name,
        product_price=product_data.product_price,
        product_description=product_data.product_description,
    )

    # Match Pydantic field names
    new_product.benefits = [
        ProductBenefits(**b.model_dump()) for b in product_data.benefits
    ]
    new_product.specification = [
        ProductSpecifications(**s.model_dump()) for s in product_data.specification
    ]
    new_product.installation_gallery = [
        ORMGallery(**g.model_dump()) for g in product_data.installation_gallery
    ]

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return ProductResponse.model_validate(new_product)


@router.get("/all", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.is_archived == False).all()
    return [ProductResponse.model_validate(p) for p in products]

# --------------------- GET PRODUCTS BY CATEGORY ---------------------
@router.get("/category/{category_name}", response_model=List[ProductResponse])
def get_products_by_category(category_name: str, db: Session = Depends(get_db)):
    products = (
        db.query(Product)
        .filter(Product.category == category_name, Product.is_archived == False)
        .all()
    )

    if not products:
        raise HTTPException(
            status_code=404,
            detail=f"No active products found for category '{category_name}'",
        )

    return [ProductResponse.model_validate(p) for p in products]



# --------------------- ARCHIVE PRODUCT ---------------------
@router.put("/archive/{product_id}")
def archive_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.is_archived:
        raise HTTPException(status_code=400, detail="Product is already archived")

    product.is_archived = True
    db.commit()
    db.refresh(product)

    return {"message": "Product archived successfully", "id": product.id}


# --------------------- UNARCHIVE PRODUCT ---------------------
@router.put("/unarchive/{product_id}")
def unarchive_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if not product.is_archived:
        raise HTTPException(status_code=400, detail="Product is not archived")

    product.is_archived = False
    db.commit()
    db.refresh(product)

    return {"message": "Product restored successfully", "id": product.id}


# --------------------- GET ARCHIVED PRODUCTS ---------------------
@router.get("/archived", response_model=List[ProductResponse])
def get_archived_products(db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.is_archived == True).all()

    if not products:
        return []

    return [ProductResponse.model_validate(p) for p in products]

# --------------------- GET SINGLE PRODUCT ---------------------
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = (
        db.query(Product)
        .filter(Product.id == product_id, Product.is_archived == False)
        .first()
    )

    if not product:
        raise HTTPException(status_code=404, detail="Product not found or archived")

    return ProductResponse.model_validate(product)
