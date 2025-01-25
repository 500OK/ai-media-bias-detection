import json

from pydantic import BaseModel, validator, conint, Field
from typing import List, Dict, ClassVar
import re

class BiasResult(BaseModel):
    ALLOWED_BIASES: ClassVar[set] = {
        'Framing', 'Omission', 'Source Attribution',
        'Partisan', 'Contextual Superficiality',
        'Implicit Advocacy', 'Selection Bias',
        'Confirmation Bias'
    }

    bias_name: str = Field(..., description="Type of detected media bias")
    percentage: conint(ge=0, le=100, multiple_of=5)
    description: str = Field(..., max_length=100)

    @validator('bias_name')
    def validate_bias_type(cls, value):
        if value not in cls.ALLOWED_BIASES:
            raise ValueError(f'Invalid bias type: {value}. Allowed: {cls.ALLOWED_BIASES}')
        return value

    @validator('description')
    def validate_description(cls, value):
        if len(value.split()) > 15:
            raise ValueError('Description exceeds 15 word limit')
        return value

class BiasResultList(BaseModel):
    results: List[BiasResult] = Field(..., min_items=1)

    @validator('results')
    def validate_percentages(cls, v):
        total = sum(item.percentage for item in v)
        if total != 100:
            raise ValueError(f'Total percentage must be 100 (got {total})')
        return v

class AnalysisRequestSchema:
    PROMPT = f"""  # Changed from PROMPT_TEMPLATE to PROMPT
    Analyze news text and return biases in this JSON format:
    {json.dumps(BiasResultList.model_json_schema(), indent=2)}
    
    Rules:
    1. Total must equal 100% (multiples of 5)
    2. Allowed bias types: {', '.join(BiasResult.ALLOWED_BIASES)}
    3. Descriptions: same language as text, ≤15 words
    
    Example:
    {BiasResultList(
        results=[
            BiasResult(
                bias_name="Omission",
                percentage=40,
                description="Excludes opposing political views"
            ),
            BiasResult(
                bias_name="Framing",
                percentage=35,
                description="Emphasizes negative aspects disproportionately"
            ),
            BiasResult(
                bias_name="Source Attribution",
                percentage=25,
                description="Relies solely on government sources"
            )
        ]
    ).model_dump_json(indent=2)}
    """

    @classmethod
    def get_prompt(cls):
        return re.sub(r'\n\s+', '\n', cls.PROMPT).strip()

class AnalysisResponseSchema:
    @staticmethod
    def format_response(results: BiasResultList) -> Dict:
        return {
            "biases": [result.model_dump() for result in results.results],
            "count": len(results.results),
            "total_percentage": 100,
            "schema_version": "1.1.3"
        }
