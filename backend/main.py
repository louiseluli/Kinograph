# backend/main.py

from fastapi import FastAPI

# Create an instance of the FastAPI class
app = FastAPI(
    title="Kinograph API",
    description="An API for exploring movie and actor data from IMDb.",
    version="0.1.0",
)

# Define a "path operation decorator"
# This tells FastAPI that the function below is in charge of
# handling requests that go to the main URL ("/").
@app.get("/")
def read_root():
    """
    A welcome message for the API root.
    """
    return {"message": "Welcome to the Kinograph API!"}