from src.startup.app import app



@app.get("/")
def read_root():
    return {"Hello": "World"}
