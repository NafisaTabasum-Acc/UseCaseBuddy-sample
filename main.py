from fastapi import FastAPI
from pydantic import AllowInfNan, BaseModel
from typing import List

app = FastAPI(title="UseCas Buddy App")

usecases = []
counter = 1

#allowed checkbox options
ALLOWED_TYPES = ["Application", "Automation", "Business Site"]



class UseCase(BaseModel):
    name: str
    description: str
    build_types: List[str] #checkbox-like multiple selection

@app.get("/")
def welcome():
    return {"message": "Welcome to the UseCase Buddy App"}

# post usecase
@app.post("/usecase")
def create_usecase(usecase: UseCase):
    global counter

    #validation (only allowed values)
    for build_type in usecase.build_types:
        if build_type not in ALLOWED_TYPES:
            return {
                "error": f"Invalid build type: {build_type}. Allowed: {ALLOWED_TYPES}"
            }
    
    data = {
        "id": counter,
        "name": usecase.name,
        "description": usecase.description,
        "build_types": usecase.build_types
    }

    usecases.append(data)
    counter += 1

    return {"message": "Use case created successfully", "id": data["id"]}

@app.get("/usecases")
def get_usecases():
    return usecases

@app.get("/usecase/{usecase_id}")
def get_usecase(usecase_id: int):
    for usecase in usecases:
        if usecase["id"] == usecase_id:
            return usecase
    return {"error": "Use case not found"}

    