from redis import Redis
from app.config import config
import asyncio
from quart import Response, Blueprint, request, jsonify, render_template
from app.services.deepseek import DeepSeekAnalyzer
from app.utils.exceptions import handle_api_error
from app.schemas.analysis import AnalysisRequestSchema, AnalysisResponseSchema, BiasResultList
from pydantic import ValidationError
from app.services.analysis_image import process_image

# Define blueprint and Redis connection
analysis_bp = Blueprint('analysis', __name__, url_prefix='/')
redis = None  # Placeholder for Redis connection

async def get_redis():
    global redis
    if redis is None:
        redis = Redis(
            host=config.REDIS_URL,
            port=config.REDIS_PORT,
            decode_responses=True,
            username=config.REDIS_USERNAME,
            password=config.REDIS_PASSWORD
        )
    return redis

async def increment_counter(key: str):
    redis_conn = await get_redis()
    redis_conn.incr(key)

@analysis_bp.before_app_serving
async def setup_redis():
    await get_redis()

@analysis_bp.route('/')
async def index():
    await increment_counter("site_visits")
    return await render_template('text_analysis.html')

@analysis_bp.route('/text-analysis')
async def text_analysis():
    await increment_counter("site_visits")
    return await render_template('text_analysis.html')

@analysis_bp.route('/image-analysis')
async def image_analysis():
    await increment_counter("site_visits")
    return await render_template('image_analysis.html')

@analysis_bp.route('/video-analysis')
async def video_analysis():
    await increment_counter("site_visits")
    return await render_template('video_analysis.html')

@analysis_bp.route('/analyze', methods=['POST'])
@handle_api_error
async def analyze_news():
    await increment_counter("processed_requests")
    data = await request.get_json()
    
    if not (text := data.get('text')):
        return jsonify({"error": "Missing required 'text' parameter"}), 400

    analyzer = DeepSeekAnalyzer()
    raw_result = await analyzer.analyze_text(text, AnalysisRequestSchema.get_prompt())
    
    try:
        validated_result = BiasResultList(**raw_result)
        return jsonify(validated_result.model_dump()), 200
    except ValidationError as e:
        return jsonify({
            "error": "Response validation error",
            "details": str(e),
            "received_data": raw_result
        }), 500

@analysis_bp.route('/analyze-image', methods=['POST'])
async def analyze_image():
    await increment_counter("processed_requests")
    try:
        files = await request.files
        if 'image' not in files:
            return jsonify(error="No image file provided"), 400
            
        file = files['image']
        
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            return jsonify(error="Invalid file type. Only PNG/JPG/JPEG allowed"), 400
            
        extracted_text, error = await process_image(file)
        if error:
            return jsonify(error=error), 400
            
        analyzer = DeepSeekAnalyzer()
        analysis_result = await analyzer.analyze_text(
            extracted_text, 
            AnalysisRequestSchema.get_prompt()
        )
        
        validated_result = BiasResultList(**analysis_result)
        return jsonify({
            "extracted_text": extracted_text,
            "analysis": validated_result.model_dump()
        }), 200
        
    except ValidationError as e:
        return jsonify({
            "error": "Response validation error",
            "details": str(e)
        }), 500
    except Exception as e:
        return jsonify(error=str(e)), 500

@analysis_bp.route('/stats')
async def stats():
    redis_conn = await get_redis()
    visits = redis_conn.get("site_visits") or 0
    processed_requests = redis_conn.get("processed_requests") or 0
    return jsonify({
        "site_visits": visits,
        "processed_requests": processed_requests
    })

@analysis_bp.route('/stats/live')
async def live_stats():
    async def event_stream():
        redis_conn = await get_redis()
        while True:
            site_visits = redis_conn.get("site_visits") or 0
            processed_requests = redis_conn.get("processed_requests") or 0
            
            data = f"data: {{\"site_visits\": {site_visits}, \"processed_requests\": {processed_requests}}}\n\n"
            yield data
            await asyncio.sleep(3)  # Send updates every 3 seconds

    return Response(event_stream(), content_type="text/event-stream")
