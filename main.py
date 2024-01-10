from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "This root endpoint."}

# routers import and api routes will be included belowfrom routers import services_router
from routers import todo_routers
app.include_router(todo_routers.router)
from routers import user_routers
app.include_router(user_routers.router)
from routers import todo_item_routers
app.include_router(todo_item_routers.router)