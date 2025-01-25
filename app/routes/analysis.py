from quart import Blueprint, request, jsonify
from app.services.deepseek import DeepSeekAnalyzer
from app.utils.exceptions import handle_api_error
from app.schemas.analysis import AnalysisRequestSchema

analysis_bp = Blueprint('analysis', __name__, url_prefix='/')

@analysis_bp.route('/analyze', methods=['POST'])
@handle_api_error
async def analyze_news():
    data = await request.get_json()

    if not (text := data.get('text')):
        return jsonify({"error": "Missing required 'text' parameter"}), 400

    analyzer = DeepSeekAnalyzer()
    result = await analyzer.analyze_text(text, AnalysisRequestSchema.get_prompt())
    return jsonify(result), 200