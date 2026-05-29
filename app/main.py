"""Main Flask application for CineMatch"""

import logging
from flask import Flask, request
from app.config import BASE_DIR
from werkzeug.exceptions import HTTPException

from app.config import APP_NAME, DEBUG, SECRET_KEY, FLASK_ENV
from app.routes.web import web_bp
from app.routes.api import api_bp

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app():
    """Create and configure Flask application."""
    # Use frontend templates and static folders
    templates_path = str(BASE_DIR / 'frontend' / 'templates')
    static_path = str(BASE_DIR / 'frontend' / 'static')
    app = Flask(__name__, template_folder=templates_path, static_folder=static_path, static_url_path='/static')
    
    # Configuration
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['DEBUG'] = DEBUG
    app.config['ENV'] = FLASK_ENV
    
    # Register blueprints
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return {'success': False, 'message': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        logger.error(f"Error: {error}")
        return {'success': False, 'message': 'Internal error'}, 500
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """Handle HTTP exceptions."""
        return {'success': False, 'message': e.description}, e.code

    # Request logging
    @app.before_request
    def log_request():
        """Log incoming requests."""
        logger.debug(f"{request.method} {request.path}")
    
    # App info endpoint
    @app.route('/info')
    def app_info():
        """Get application information."""
        return {
            'app_name': APP_NAME,
            'version': '1.0.0',
            'environment': FLASK_ENV,
            'endpoints': {
                'web': '/',
                'api': '/api/v1',
                'analytics': '/api/v1/analytics'
            }
        }
    
    logger.info(f"CineMatch application created in {FLASK_ENV} mode")
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)
