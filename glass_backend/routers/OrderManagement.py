from database_connector import get_db
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import APIRouter, Depends, HTTPException, Cookie,Query
from typing import List, Optional
from models.ProductModel import DashboardReportRequest
from models.OrderModel import AddOrder, OrderResponse,DeliveryAddress,AdminOrderUpdate,OrderResponseAdmin,DashboardDataResponse,PendingOrdersCountResponse,OrderLogResponse,RejectOrderPayload
from database.ProductTable import Orders as TableOrders, OrderItem, OrderStatus, Product,DashboardData,OrderLog
from database.UsersAccountTable import Address, User 
from datetime import datetime,timedelta
import tools
from jwt_handler import get_current_user 
router = APIRouter(prefix="/orders", tags=["Cart & Orders"])


# =========================
# 🛒 Add Order (with active address) and update Product Stock
# =========================
@router.post("/add-order", response_model=OrderResponse)
def add_order(order_data: AddOrder, user_email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user_email:
        raise HTTPException(status_code=401, detail="User not found")

    # ✅ Check product existence
    product = db.query(Product).filter(Product.id == order_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # ✅ Get user by email
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ Get active address for user
    active_address = (
        db.query(Address)
        .filter(Address.user_id == user.user_id, Address.is_active == True)
        .first()
    )
    if not active_address:
        raise HTTPException(status_code=400, detail="No active address found. Please set one before ordering.")

    # ✅ Always create a new order
    order = TableOrders(
        user_email=user_email,
        status=OrderStatus.Pending,
        house_number=active_address.house_number,
        street=active_address.street,
        barangay=active_address.barangay,
        city=active_address.city,
        province=active_address.province,
        order_note=order_data.order_note
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    # ✅ Add new order item
    new_item = OrderItem(
        order_id=order.id,
        product_id=product.id,
        quantity=order_data.quantity,
        product_name=product.product_name,
        product_category=product.category,
        product_type=product.product_type,
        product_price=product.product_price,
        product_image=product.product_image,
    )

    db.add(new_item)



    from database.AdminTable import RecentActivity
    import tools
    from datetime import datetime

    recent_activity = RecentActivity(
        user_email=user_email,
        action="Order",
        detail=f"Order #{order.id} - {product.product_name}",
        created_at=datetime.now(tools.PH_TZ)
    )

    db.add(recent_activity)
    db.commit()
    db.refresh(recent_activity)

    # ✅ Return full response (with updated stock info)
    return OrderResponse(
        order_id=order.id,
        status=order.status.value,
        created_at=order.created_at,
        product_image=product.product_image,
        product_category=product.category,
        product_type=product.product_type,
        product_name=product.product_name,
        product_price=product.product_price,
        quantity=new_item.quantity,
        total_price=product.product_price * new_item.quantity,
        order_note=order_data.order_note,
        delivery_address=DeliveryAddress(
            house_number=order.house_number,
            street=order.street,
            barangay=order.barangay,
            city=order.city,
            province=order.province
        )
    )



# =========================
# 📦 Get Orders (with address)
# =========================
@router.get("/", response_model=list[OrderResponse])
def get_orders(
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user)  # ✅ Use JWT instead of cookie
):
    orders = (
        db.query(TableOrders)
        .filter(TableOrders.user_email == user_email)
        .order_by(TableOrders.created_at.desc())
        .all()
    )

    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")

    responses = []
    for order in orders:
        order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
        for item in order_items:
            responses.append(
                OrderResponse(
                    order_id=order.id,
                    status=order.status.value,
                    created_at=order.created_at,
                    product_image=item.product_image,
                    product_category=item.product_category,
                    product_type=item.product_type,
                    product_name=item.product_name,
                    product_price=item.product_price,
                    quantity=item.quantity,
                    total_price=item.product_price * item.quantity,
                    order_note=order.order_note,
                    delivery_address=DeliveryAddress(
                        house_number=order.house_number,
                        street=order.street,
                        barangay=order.barangay,
                        city=order.city,
                        province=order.province
                    )
                )
            )

    return responses

@router.put("/update-status/{order_id}")
def update_order_status(
    order_id: int,
    status_data: AdminOrderUpdate,
    db: Session = Depends(get_db)
    ):
    order = db.query(TableOrders).filter(TableOrders.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    valid_statuses = [status.value for status in OrderStatus]
    if status_data.status.lower() not in [s.lower() for s in valid_statuses]:
        raise HTTPException(status_code=400, detail=f"Invalid status. Valid options: {valid_statuses}")

    # ✅ Update order status
    order.status = OrderStatus(status_data.status)
    db.commit()
    db.refresh(order)

    # ✅ If status becomes Installed or Rejected, insert snapshot into OrderLog
    if order.status in [OrderStatus.Installed, OrderStatus.Reject]:
        order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
        for item in order_items:
            log_entry = OrderLog(
                order_id=order.id,
                user_email=order.user_email,
                created_at=order.created_at,
                status=order.status,
                house_number=order.house_number,
                street=order.street,
                barangay=order.barangay,
                city=order.city,
                province=order.province,
                product_id=item.product_id,
                product_category=item.product_category,
                product_type=item.product_type,
                product_image=item.product_image,
                product_name=item.product_name,
                product_price=item.product_price,
                quantity=item.quantity,
                order_note=order.order_note,
            )
            db.add(log_entry)
        db.commit()

    # ✅ If status becomes Installed or Shipped, populate DashboardData
    if order.status in [OrderStatus.Installed]:
        order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
        for item in order_items:
            dashboard_entry = DashboardData(
                product_category=item.product_category,
                product_name=item.product_name,
                product_quantity=item.quantity,
                product_price=item.product_price,
                order_date=order.created_at
            )
            db.add(dashboard_entry)
        db.commit()

    return {"message": f"Order {order_id} status updated to {order.status.value}"}

# ------------------------------
# Delete order endpoint
# ------------------------------
@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(TableOrders).filter(TableOrders.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()

    # ✅ Insert into OrderLog before deleting
    for item in order_items:
        log_entry = OrderLog(
            order_id=order.id,
            user_email=order.user_email,
            created_at=order.created_at,
            status=order.status,
            house_number=order.house_number,
            street=order.street,
            barangay=order.barangay,
            city=order.city,
            province=order.province,
            product_id=item.product_id,
            product_category=item.product_category,
            product_type=item.product_type,
            product_image=item.product_image,
            product_name=item.product_name,
            product_price=item.product_price,
            quantity=item.quantity,
            order_note=order.order_note,
        )
        db.add(log_entry)
    db.commit()

    # Delete order items and order
    db.query(OrderItem).filter(OrderItem.order_id == order.id).delete()
    db.delete(order)
    db.commit()

    return {"message": f"Order {order_id} has been deleted successfully."}

@router.get("/order-admin", response_model=list[OrderResponseAdmin])
def get_all_orders(db: Session = Depends(get_db)):
    orders = db.query(TableOrders).order_by(TableOrders.created_at.desc()).all()

    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")

    responses = []
    for order in orders:
        order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
        for item in order_items:
            responses.append(
                OrderResponseAdmin(
                    order_id=order.id,
                    product_id=item.product_id,
                    user_email=order.user_email,
                    status=order.status.value,
                    created_at=order.created_at,
                    product_image=item.product_image,
                    product_category=item.product_category,
                    product_type=item.product_type,
                    product_name=item.product_name,
                    product_price=item.product_price,
                    quantity=item.quantity,
                    order_note=order.order_note,
                    total_price=item.product_price * item.quantity,
                    delivery_address=DeliveryAddress(
                        house_number=order.house_number,
                        street=order.street,
                        barangay=order.barangay,
                        city=order.city,
                        province=order.province
                    )
                )
            )
    return responses


# =========================
# 📊 Fetch Dashboard Data (for all three charts)
# =========================
@router.get("/dashboard-data", response_model=List[DashboardDataResponse])
def get_dashboard_data(db: Session = Depends(get_db)):
    from datetime import datetime, timedelta

    today = datetime.now(tools.PH_TZ)
    seven_days_ago = today - timedelta(days=7)

    data_rows = (
        db.query(DashboardData)
        .filter(DashboardData.order_date >= seven_days_ago)
        .order_by(DashboardData.order_date.desc())
        .all()
    )

    return [
        DashboardDataResponse(
            id=row.id,
            product_category=row.product_category,
            product_name=row.product_name,
            product_quantity=row.product_quantity,
            product_price=float(row.product_price),
            order_date=row.order_date,
        )
        for row in data_rows
    ]

@router.post("/dashboard-report", response_model=list[DashboardDataResponse])
def get_dashboard_report(payload: DashboardReportRequest, db: Session = Depends(get_db)):
    try:
        start_dt = datetime.strptime(payload.start_date, "%Y-%m-%d").replace(tzinfo=tools.PH_TZ)
        end_dt = datetime.strptime(payload.end_date, "%Y-%m-%d").replace(tzinfo=tools.PH_TZ)

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    # Query within range
    data_rows = (
        db.query(DashboardData)
        .filter(and_(DashboardData.order_date >= start_dt, DashboardData.order_date <= end_dt))
        .order_by(DashboardData.order_date.asc())
        .all()
    )

    if not data_rows:
        raise HTTPException(status_code=404, detail="No data found for the selected date range.")

    return [
        DashboardDataResponse(
            id=row.id,
            product_category=row.product_category,
            product_name=row.product_name,
            product_quantity=row.product_quantity,
            product_price=float(row.product_price),
            order_date=row.order_date,
        )
        for row in data_rows
    ]

@router.get("/pending-orders-count", response_model=PendingOrdersCountResponse)
def get_pending_orders_count(db: Session = Depends(get_db)):
    count = db.query(TableOrders).filter(TableOrders.status == OrderStatus.Pending).count()
    return PendingOrdersCountResponse(pending_count=count)

# =========================
# 📜 Get Order Log
# =========================
@router.get("/order-log", response_model=list[OrderLogResponse])
def get_order_log(db: Session = Depends(get_db)):
    logs = db.query(OrderLog).order_by(OrderLog.created_at.desc()).all()
    
    if not logs:
        raise HTTPException(status_code=404, detail="No order logs found")
    
    response = []
    for log in logs:
        response.append(
            OrderLogResponse(
                id=log.id,
                order_id=log.order_id,
                user_email=log.user_email,
                created_at=log.created_at,
                status=log.status.value if isinstance(log.status, OrderStatus) else log.status,
                reject_reason=log.reject_reason,
                order_note=log.order_note,
                delivery_address={
                    "house_number": log.house_number or "",
                    "street": log.street or "",
                    "barangay": log.barangay or "",
                    "city": log.city or "",
                    "province": log.province or ""
                },
                product_id=log.product_id,
                product_category=log.product_category,
                product_type=log.product_type,
                product_image=log.product_image,
                product_name=log.product_name,
                product_price=log.product_price,
                quantity=log.quantity
            )
        )
    
    return response

# ------------------------------
# ✏️ Update product price (Admin Only)
# ------------------------------
@router.put("/update-price/{order_id}")
def update_order_price(
    order_id: int,
    payload: dict,
    db: Session = Depends(get_db)
):
    # Validate payload
    new_price = payload.get("product_price")
    if new_price is None:
        raise HTTPException(status_code=400, detail="Missing product_price field")

    # ✅ Fetch the order
    order = db.query(TableOrders).filter(TableOrders.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # ✅ Ensure only processing orders can be edited
    if order.status != OrderStatus.Processing:
        raise HTTPException(status_code=400, detail="Price can only be updated while order is still Processing")

    # ✅ Fetch order items
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    if not order_items:
        raise HTTPException(status_code=404, detail="No items found for this order")

    # ✅ Update each order item’s price
    for item in order_items:
        item.product_price = new_price
        db.add(item)

    db.commit()

    return {"message": f"Order {order_id} price updated to ₱{new_price}"}

@router.put("/reject-order/{order_id}")
def reject_order(order_id: int, payload: RejectOrderPayload, db: Session = Depends(get_db)):
    order = db.query(TableOrders).filter(TableOrders.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Update order status and reject reason
    order.status = OrderStatus.Reject
    order.reject_reason = payload.reason   # <--- store reason in main table
    db.commit()
    db.refresh(order)

    # Insert reason into OrderLog for each item
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    for item in order_items:
        log_entry = OrderLog(
            order_id=order.id,
            user_email=order.user_email,
            created_at=order.created_at,
            status=order.status,
            house_number=order.house_number,
            street=order.street,
            barangay=order.barangay,
            city=order.city,
            province=order.province,
            product_id=item.product_id,
            product_category=item.product_category,
            product_type=item.product_type,
            product_image=item.product_image,
            product_name=item.product_name,
            product_price=item.product_price,
            quantity=item.quantity,
            reject_reason=payload.reason,
            order_note=order.order_note,

        )
        db.add(log_entry)
    db.commit()

    return {"message": f"Order {order_id} has been rejected", "reason": payload.reason}
