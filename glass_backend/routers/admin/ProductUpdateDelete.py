from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database_connector import get_db
from models.ProductModel import (
    ProductResponse,
    AdminProductUpdate,
)
from database.ProductTable import Product, ProductBenefits, ProductSpecifications, InstallationGallery as ORMGallery

router = APIRouter(prefix="/product", tags=["product"])

# --------------------- UPDATE PRODUCT ---------------------
@router.put("/update/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_data: AdminProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_fields = product_data.model_dump(exclude_unset=True)

    # Update simple fields
    for field, value in update_fields.items():
        if field not in ["key_benefits", "specification", "gallery"]:
            setattr(product, field, value)

    # Update nested fields
    if "key_benefits" in update_fields:
        product.benefits = [ProductBenefits(**b) for b in update_fields["key_benefits"]]
    if "specification" in update_fields:
        product.specification = [ProductSpecifications(**s) for s in update_fields["specification"]]
    if "gallery" in update_fields:
        product.installation_gallery = [ORMGallery(**g) for g in update_fields["gallery"]]

    db.commit()
    db.refresh(product)

    return ProductResponse.model_validate(product)

# --------------------- DELETE PRODUCT ---------------------
@router.delete("/delete/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return {"message": f"Product with ID {product_id} has been successfully deleted."}

