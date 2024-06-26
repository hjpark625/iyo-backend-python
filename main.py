from fastapi import FastAPI
from detail.app import router as detail_router
from pins.app import router as pins_router
from auth.app import router as auth_router
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
app.include_router(auth_router)


@app.get("/")
def __main__():
    return {"message": "Server is Running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=4000, reload=True)
