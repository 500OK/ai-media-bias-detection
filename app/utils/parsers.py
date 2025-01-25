import json
from typing import List, Dict
from pydantic import BaseModel, validator

class BiasResult(BaseModel):
    bias_name: str
    percentage: float
    description: str

    @validator('percentage')
    def validate_percentage(cls, value):
        if not (0 <= value <= 100):
            raise ValueError("Percentage must be between 0-100")
        return value

def validate_bias_results(data: List[Dict]) -> List[BiasResult]:
    if not isinstance(data, list):
        raise ValueError("Expected list of results")
        
    return [BiasResult(**item) for item in data]