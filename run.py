"""
Recipe Assistant Bot - Main Application Runner
Author: RSK World (https://rskworld.in)
Founder: Molla Samser
Designer & Tester: Rima Khatun
Contact: help@rskworld.in, +91 93305 39277
Year: 2026
"""

import os
from app import create_app
from config import get_config

# Get configuration based on environment
config_class = get_config()
app = create_app()

# Configure app with the selected config
app.config.from_object(config_class)

if __name__ == '__main__':
    # Development server
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    debug = app.config.get('DEBUG', False)
    
    print(f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║           Recipe Assistant Bot - RSK World                   ║
    ╠══════════════════════════════════════════════════════════════╣
    ║  Version: 1.0.0                                              ║
    ║  Author: RSK World                                           ║
    ║  Founder: Molla Samser                                       ║
    ║  Designer & Tester: Rima Khatun                             ║
    ║  Contact: help@rskworld.in, +91 93305 39277                 ║
    ║  Website: https://rskworld.in                               ║
    ║  Year: 2026                                                  ║
    ╠══════════════════════════════════════════════════════════════╣
    ║  Starting server...                                          ║
    ║  URL: http://{host}:{port}                                   ║
    ║  Debug Mode: {debug}                                          ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    app.run(host=host, port=port, debug=debug)
