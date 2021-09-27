from fastapi import FastAPI

from service.app.api.methods import xMethods

app = FastAPI()

app.include_router(xMethods)
