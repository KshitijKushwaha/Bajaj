from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, validator
import base64
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to your React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestModel(BaseModel):
    data: List[str]
    file_b64: str = None

    @validator('data')
    def data_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('data list must not be empty')
        return v


class ResponseModel(BaseModel):
    is_success: bool
    user_id: str
    email: str
    roll_number: str
    numbers: list
    alphabets: list
    highest_lowercase_alphabet: list
    file_valid: bool
    file_mime_type: Optional[str] = None  # Make this optional
    file_size_kb: Optional[float] = None  # Make this optional


def process_data(data):
    numbers = [x for x in data if x.isdigit()]
    alphabets = [x for x in data if x.isalpha()]
    highest_lowercase = [max([x for x in alphabets if x.islower()])] if any(x.islower() for x in alphabets) else []
    return numbers, alphabets, highest_lowercase

def decode_file(file_b64):
    try:
        file_data = base64.b64decode(file_b64)
        file_size = len(file_data) / 1024  # in KB
        # Assume it's an image/png for the sake of the example
        file_mime_type = "image/png"
        return True, file_mime_type, file_size
    except Exception:
        return False, None, None

@app.post("/bfhl")
async def process_request(request: RequestModel):
    try:
        numbers, alphabets, highest_lowercase = process_data(request.data)
        
        file_valid, file_mime_type, file_size_kb = decode_file(request.file_b64) if request.file_b64 else (False, None, None)
        
        response = ResponseModel(
            is_success=True,
            user_id="john_doe_17091999",
            email="john@xyz.com",
            roll_number="ABCD123",
            numbers=numbers,
            alphabets=alphabets,
            highest_lowercase_alphabet=highest_lowercase,
            file_valid=file_valid,
            file_mime_type=file_mime_type,
            file_size_kb=file_size_kb
        )
        return response
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.get("/bfhl")
async def get_operation_code():
    return {"operation_code": 1}

