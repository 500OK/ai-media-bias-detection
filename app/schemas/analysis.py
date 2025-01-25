import json

from pydantic import BaseModel, validator, conint, Field
from typing import List, Dict, ClassVar
import re

class BiasResult(BaseModel):
    bias_name: str = Field(..., description="Type of detected media bias")
    percentage: float
    description: str = Field(..., max_length=300)

    @validator('description')
    def validate_description(cls, value):
        if len(value.split()) > 100:
            raise ValueError('Description exceeds 30 word limit')
        return value

    @validator('percentage')
    def validate_percentage(cls, value):
        if not (0 <= value <= 100):
            raise ValueError("Percentage must be between 0-100")
        return value

class BiasResultList(BaseModel):
    results: List[BiasResult] = Field(..., min_items=1)

class AnalysisRequestSchema:
    PROMPT = """
    Analyze news text and return detected biases in this exact JSON format:
    {
        "results": [
            {
                "bias_name": "string",
                "description": "string",
                "percentage": number
            }
        ]
    }
    
    Rules:
    1. Each bias should be evaluated independently from 0 to 100%
    2. The sum of percentages doesn't need to equal 100%
    3. Descriptions and bias names MUST be in the same language as the input text
    4. Identify all potential biases present in the text
    5. Use natural language terms for bias names that match the input text's language
    
    Example for English:
    {
        "results": [
            {
                "bias_name": "Political Bias",
                "description": "Favors one political side",
                "percentage": 45
            },
            {
                "bias_name": "Omission",
                "description": "Ignores important counterarguments",
                "percentage": 30
            }
        ]
    }

    Example for Romanian text:
    {
        "results": [
            {
                "bias_name": "Părtinire Politică",
                "description": "Textul favorizează o anumită poziție politică",
                "percentage": 45
            },
            {
                "bias_name": "Omisiune",
                "description": "Lipsesc informații importante despre contraargumente",
                "percentage": 30
            }
        ]
    }
    """

    @classmethod
    def get_prompt(cls):
        return re.sub(r'\n\s+', '\n', cls.PROMPT).strip()

class AnalysisResponseSchema(BaseModel):
    results: List[BiasResult]

    @validator('results')
    def validate_results(cls, value):
        if not value:
            raise ValueError("At least one bias result is required")
        return value

    @staticmethod
    def format_response(results: BiasResultList) -> Dict:
        return {
            "results": [result.model_dump() for result in results.results]
        }
