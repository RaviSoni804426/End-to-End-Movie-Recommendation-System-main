"""Run script for CineMatch"""

import os
from app.main import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False') == 'True'
    app.run(debug=debug, host='0.0.0.0', port=port)
