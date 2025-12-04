from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database_connector import get_db
from database.UsersAccountTable import Address as AddressTable, User
from models.UserModel import Address, AddressResponse, ActivateAddress
from jwt_handler import get_current_user  # ✅ Import JWT helper
from datetime import datetime
import tools

router = APIRouter(prefix="/users", tags=["users"])


# ---------------- Get All Addresses ----------------
@router.get("/addresses", response_model=list[AddressResponse])
def get_addresses(user_email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    addresses = db.query(AddressTable).filter(AddressTable.user_id == user.user_id).all()
    return addresses


# ---------------- Add New Address ----------------
@router.post("/address/add", response_model=AddressResponse)
def add_address(address: Address, user_email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_address = AddressTable(
        user_id=user.user_id,
        house_number=address.house_number,
        street=address.street,
        barangay=address.barangay,
        city=address.city,
        province=address.province,
        is_active=False
    )

    db.add(new_address)
    db.commit()
    db.refresh(new_address)

    # Log Recent Activity
    from database.AdminTable import RecentActivity

    address_detail = f"{address.house_number}, {address.street}, {address.barangay}, {address.city}, {address.province}"

    recent_activity = RecentActivity(
        user_email=user_email,
        action="Added New Address",
        detail=address_detail,
        created_at=datetime.now(tools.PH_TZ)
    )

    db.add(recent_activity)
    db.commit()
    db.refresh(recent_activity)

    return new_address


# ---------------- Activate Address ----------------
@router.put("/address/{address_id}/activate", response_model=AddressResponse)
def activate_address(address_id: int, request: ActivateAddress, db: Session = Depends(get_db)):
    address = db.query(AddressTable).filter(AddressTable.id == address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    if request.is_active:
        # Deactivate all other addresses for this user
        db.query(AddressTable).filter(AddressTable.user_id == address.user_id).update(
            {AddressTable.is_active: False}
        )
        address.is_active = True
    else:
        address.is_active = False

    db.commit()
    db.refresh(address)
    return address


# ---------------- Delete Address ----------------
@router.delete("/address/{address_id}", response_model=AddressResponse)
def delete_address(address_id: int, user_email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    address = db.query(AddressTable).filter(AddressTable.id == address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    db.delete(address)
    db.commit()
    return address
