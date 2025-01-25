from quart import Blueprint, request, jsonify, render_template
from app.services.deepseek import DeepSeekAnalyzer
from app.utils.exceptions import handle_api_error
from app.schemas.analysis import AnalysisRequestSchema, AnalysisResponseSchema, BiasResultList
from pydantic import ValidationError

analysis_bp = Blueprint('analysis', __name__, url_prefix='/')

@analysis_bp.route('/')
async def index():
    return await render_template('text_analysis.html')

@analysis_bp.route('/text-analysis')
async def text_analysis():
    return await render_template('text_analysis.html')

@analysis_bp.route('/image-analysis')
async def image_analysis():
    return await render_template('image_analysis.html')

@analysis_bp.route('/video-analysis')
async def video_analysis():
    return await render_template('video_analysis.html')

@analysis_bp.route('/analyze', methods=['POST'])
@handle_api_error
async def analyze_news():
    data = await request.get_json()
    
    if not (text := data.get('text')):
        return jsonify({"error": "Missing required 'text' parameter"}), 400

    analyzer = DeepSeekAnalyzer()
    raw_result = await analyzer.analyze_text(text, AnalysisRequestSchema.get_prompt())
    
    try:
        # Validate the response structure
        validated_result = BiasResultList(**raw_result)
        return jsonify(validated_result.model_dump()), 200
    except ValidationError as e:
        return jsonify({
            "error": "Response validation error",
            "details": str(e),
            "received_data": raw_result
        }), 500


@analysis_bp.route('/analyze_fun', methods=['POST'])
@handle_api_error
async def analyze_news_fun():
    data = await request.get_json()

    if not (text := data.get('text')):
        return jsonify({"status": "Internal Server Error", "message": "Missing 'text' parameter"}), 200  # 😈

    analyzer = DeepSeekAnalyzer()
    result = await analyzer.analyze_text(text, AnalysisRequestSchema.get_prompt())
    return jsonify({"status": "OK", "data": result}), 500  # 😈

@analysis_bp.route('/', methods=['GET'])
async def show_form():
    return await render_template('analyze_form.html')

@analysis_bp.route('/analyze-image', methods=['POST'])
async def analyze_image():
    try:
        file = (await request.files)['image']
        
        # Process image
        extracted_text, error = await process_image(file)
        if error:
            return jsonify(error=error), 400
            
        # Send text to existing bias analysis
        bias_response = await analyze_text(extracted_text)
        return bias_response
        
    except Exception as e:
        return jsonify(error=str(e)), 500