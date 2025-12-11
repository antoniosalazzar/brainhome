from fastapi import FastAPI

app = FastAPI(title="HomeBrain API")

@app.get("/")
def root():
    return {"message": "HomeBrain is running"}

