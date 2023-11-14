import sys
import os

logger_path = sys.path[0].replace('LASER', 'LOGGER')

try : 
    sys.path.append(logger_path)
except :
    print("Error during import of path")

from LOGGER.logger import logger
logger.log_camera_acquisition()