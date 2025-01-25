import json
from typing import List, Dict
from pydantic import BaseModel, validator

class BiasResult(BaseModel):
    bias_name: str
    percentage: int
    description: str

    @validator('percentage')
    def validate_percentage(cls, value):
        if not (0 <= value <= 100) or value % 5 != 0:
            raise ValueError("Percentage must be multiple of 5 between 0-100")
        return value

def validate_bias_results(data: List[Dict]) -> List[BiasResult]:
    results = [BiasResult(**item) for item in data]

    total = sum(item.percentage for item in results)
    if total != 100:
        raise ValueError(f"Total percentages must equal 100 (current: {total})")

    return results