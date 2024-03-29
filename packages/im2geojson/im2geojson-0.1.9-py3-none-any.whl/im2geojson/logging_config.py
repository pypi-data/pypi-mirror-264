"""
Logging configuration for CLI.
"""

import logging


logger = logging.getLogger('im2geojson')
logger.setLevel(logging.DEBUG)

# console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO) 

# formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# add console_handler to logger
logger.addHandler(console_handler)

# log configured
logger.info('logging configured')