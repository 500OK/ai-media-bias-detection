# Media Bias Detection API

A Quart-based API for detecting media biases in news articles using DeepSeek's analysis capabilities.

## Features
- Bias analysis with percentage breakdown
- Multi-language support (English/Romanian/Russian)
- Docker containerization
- JSON API responses

## Prerequisites
- Docker (version 20.10+)
- Python 3.11+
- DeepSeek API key

## Installation

### 1. Clone repository
```bash
git clone https://github.com/yourusername/ai-media-bias-detection.git
cd ai-media-bias-detection
```

### 2. Install dependencies
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configuration
Create `.env` file:
```env
DEEPSEEK_K1=your_api_key_here
```

## Docker Setup

### Build the image
```bash
docker build -t media-bias-detector .
```

### Run the container
```bash
docker run -d -p 5000:5000 \
  --env-file .env \
  --name bias-detector \
  media-bias-detector
```

### Manage container
```bash
# View logs
docker logs -f bias-detector

# Stop container
docker stop bias-detector

# Start existing container
docker start bias-detector

# Remove container
docker rm bias-detector
```

## Running Without Docker
```bash
quart run --host 0.0.0.0 --port 5000
```

## API Usage

### Request
```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Fosta bașcană a Găgăuziei, Irina Vlah... [your Romanian text]"
  }'
```

### Response Example
```json
{
  "biases": [
    {
      "bias_name": "Omission",
      "percentage": 35,
      "description": "Lipsa perspectivelor opuse pe aderarea la UE"
    },
    {
      "bias_name": "Framing",
      "percentage": 30,
      "description": "Accentuează nemulțumirea lui Vlah"
    }
  ],
  "count": 2,
  "total_percentage": 100,
  "schema_version": "1.1.3"
}
```

## Troubleshooting

### Common Errors
**Docker daemon not running**
```bash
# Start Docker Desktop (macOS/Windows)
# For Linux:
sudo systemctl start docker
```

**Invalid API key**
- Verify `.env` file contains correct DEEPSEEK_K1
- Ensure container has environment variable:
  ```bash
  docker exec bias-detector env | grep DEEPSEEK_K1
  ```

**JSON parsing errors**
- Check API response format with:
  ```bash
  docker logs bias-detector | grep "Raw API response"
  ```

## License
MIT License

---

**Contact**: [Your Name] | [Your Email] | [Project URL]
