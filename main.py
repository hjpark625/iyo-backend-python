from fastapi import FastAPI
from detail.app import router as detail_router
from pins.app import router as pins_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


# origin = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origin,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(detail_router)
app.include_router(pins_router)


@app.get("/")
def __main__():
    return {"message": "Server is Running"}
