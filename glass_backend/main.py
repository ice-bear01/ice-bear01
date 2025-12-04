from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database_connector import Base, engine
from api import include_routers
from routers.user_management import router as user_management_router
import os
import uvicorn 

#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()
# "http://localhost:5173/"
# "https://glass-v1s2.onrender.com"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_management_router)


include_routers(app)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port,reload=True)
