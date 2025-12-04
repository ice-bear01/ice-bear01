from fastapi import FastAPI
from routers.auth import UsersAccountRoute,EmailVerRoute
from routers.admin import ProductCreateRead,ProductUpdateDelete,RecentAct
from routers import OrderManagement,UserAddressEndpoint,UserRoute
def include_routers(app: FastAPI):
    app.include_router(UsersAccountRoute.router)
    app.include_router(ProductCreateRead.router)
    app.include_router(ProductUpdateDelete.router)
    app.include_router(EmailVerRoute.router)
    app.include_router(OrderManagement.router)
    app.include_router(UserAddressEndpoint.router)
    app.include_router(UserRoute.router)
    app.include_router(RecentAct.router)