import logging
import platform
import datetime

logger = logging.getLogger(__name__)

def get_system_info():
    """Get basic system information"""
    try:
        return {
            'platform': platform.system(),
            'python_version': platform.python_version(),
            'timestamp': datetime.datetime.now().isoformat(),
            'hostname': platform.node()
        }
    except Exception as e:
        logger.error(f"Error getting system info: {str(e)}")
        return {'error': 'Unable to retrieve system info'}

def validate_input(data):
    """Basic input validation"""
    try:
        if not data or not isinstance(data, dict):
            return False
        
        # Add your validation logic here
        required_fields = ['name']  # Example required field
        return all(field in data for field in required_fields)
        
    except Exception as e:
        logger.error(f"Error validating input: {str(e)}")
        return False