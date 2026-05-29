"""Run script for CineMatch"""

import os
from app.main import create_app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True') == 'True'
    app.run(debug=debug, host='0.0.0.0', port=port)
