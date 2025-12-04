from pydantic import BaseModel, ConfigDict
from typing import List, Optional

# -------------------------
# Submodels
# -------------------------
class KeyBenefits(BaseModel):
    benefit_title: str
    benefit_description: str

    model_config = ConfigDict(from_attributes=True)
class ProductSpecification(BaseModel):
    specification_title: str
    specification_description: str

    model_config = ConfigDict(from_attributes=True)
class InstallationGallery(BaseModel):
    image: str
    description: str

    model_config = ConfigDict(from_attributes=True)
# -------------------------
# Main Product Models
# -------------------------
class AddNewProduct(BaseModel):
    category: str
    product_image: str
    product_type: str
    product_name: str
    product_description: str
    product_price: float

    # ✅ Use names that match SQLAlchemy relationships
    benefits: List[KeyBenefits]
    specification: List[ProductSpecification]
    installation_gallery: List[InstallationGallery]

    model_config = ConfigDict(from_attributes=True)


class ProductResponse(AddNewProduct):
    id: int
    
class AdminProductUpdate(BaseModel):
    category: Optional[str] = None
    product_image: Optional[str] = None
    product_type: Optional[str] = None
    product_name: Optional[str] = None
    product_description: Optional[str] = None
    product_price: Optional[float] = None
    key_benefits: Optional[List[KeyBenefits]] = None
    specification: Optional[List[ProductSpecification]] = None
    gallery: Optional[List[InstallationGallery]] = None



class DashboardReportRequest(BaseModel):
    start_date: str
    end_date: str