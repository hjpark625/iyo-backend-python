from fastapi import FastAPI, HTTPException
from detail.app import router as detail_router
from pins.app import router as pins_router

app = FastAPI()

app.include_router(detail_router)
app.include_router(pins_router)


@app.get("/")
def __main__():
    return {"message": "Server is Running"}
