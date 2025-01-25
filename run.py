import json

from quart import Quart, request, jsonify
from quart_cors import cors
import httpx
import os

app = Quart("BiasAnalyzer")
app = cors(app, allow_origin="*")

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_KEY = os.getenv("DEEPSEEK_K1")  # Verify env variable exists with: echo $DEEPSEEK_K1

ANALYSIS_PROMPT = ANALYSIS_PROMPT = """Analyze the provided news text and return ALL biases in this EXACT JSON format:  
[  
  {  
    "bias_name": "[Bias Type]",  
    "percentage": [X],  
    "description": "[Concise reason in text's language]"  
  }  
]  

RULES:  
1. Total percentages MUST equal 100 (multiples of 5 only)  
2. Use ONLY these bias types:  
   - Framing  
   - Omission  
   - Source Attribution  
   - Partisan  
   - Contextual Superficiality  
   - Implicit Advocacy  
   - Selection Bias  
   - Confirmation Bias  
3. Descriptions must:  
   - Match the text's language (Russian/English/Romanian)  
   - Be under 15 words  
4. Output ONLY valid JSON (no markdown)  

EXAMPLE FOR ENGLISH TEXT:  
[  
  {  
    "bias_name": "Omission",  
    "percentage": 30,  
    "description": "Excludes opposing views on EU accession"  
  }  
]"""

@app.route('/analyze', methods=['OPTIONS', 'POST'])
async def analyze_news():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()

    try:
        data = await request.get_json()
        news_text = data.get('text')

        if not news_text:
            return jsonify({"error": "Missing 'text' parameter"}), 400

        analysis = await _get_deepseek_analysis(news_text)
        return jsonify(analysis), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

async def _get_deepseek_analysis(text: str) -> dict:
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_KEY}",
        "Content-Type": "application/json"
    }

    # Fixed payload structure
    payload = {
        "model": "deepseek-chat",  # Changed from deepseek-r1
        "messages": [
            {
                "role": "user",
                "content": f"{ANALYSIS_PROMPT}\n\nNews Text:\n{text}"
            }
        ],
        "temperature": 0.3,
        "max_tokens": 2000,  # Added required parameter
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }

    async with httpx.AsyncClient(timeout=100) as client:
        response = await client.post(DEEPSEEK_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        parsed_valid_json = parse_response(response_json)
        print(parsed_valid_json)
        return response_json

def parse_response(response):
    try:
        content_str = response['choices'][0]['message']['content']
        return json.loads(content_str)  # Double parsing
    except:
        # Fallback for malformed responses
        content_str = content_str.replace('\n','').replace('\\"','"')
        return json.loads(content_str)

def _build_cors_preflight_response():
    response = jsonify({"message": "CORS preflight successful"})
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)