from flask import Flask, render_template, request, jsonify
import logging
from .utils import get_system_info, validate_input

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

@app.route('/')
def index():
    try:
        logger.info("Index page accessed")
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    try:
        if request.method == 'POST':
            data = request.get_json()
            if not validate_input(data):
                return jsonify({'error': 'Invalid input'}), 400
            
            logger.info(f"Received POST data: {data}")
            return jsonify({
                'status': 'success',
                'message': 'Data received successfully',
                'data': data
            })
        
        # GET request
        system_info = get_system_info()
        logger.info("System info requested")
        return jsonify(system_info)
        
    except Exception as e:
        logger.error(f"Error in api_data: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health')
def health_check():
    try:
        return jsonify({'status': 'healthy', 'service': 'flask-k8s'}), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({'status': 'unhealthy'}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
