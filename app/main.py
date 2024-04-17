from fastapi import FastAPI

from app.api_v1.general import general_router


app = FastAPI()

app.include_router(general_router)
