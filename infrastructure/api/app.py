from fastapi import FastAPI 
from infrastructure.api.controllers.QueryController import router as query_router

app = FastAPI(
    title="MultiAgent"
)

app.include_router(
    query_router,
    prefix="/ws"
)