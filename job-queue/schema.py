from pydantic import BaseModel

class JobCreate(BaseModel):
    model: str
    input: str

class JobResponse(BaseModel):
    id: int
    model: str
    input: str
    status: str

class JobQuery(BaseModel):
    id: int
