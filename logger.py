import logging
import os

class Log():

    def __init__(self):
        if os.path.exists('app.log'):
            os.remove('app.log')
        logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        logging.info('Init log file')
        self.logger = logging.getLogger(__name__)

    def log_laser_connect(self):
        self.logger.info("Laser is now connected")

    def log_laser_disconnect(self):
        self.logger.info("Laser is now disconnected")

    def log_viewmeter_value(self, value):
        self.logger.info("Viewmeter acquisition at %s"%(value) + "%")

    def log_take_picture(self, name_save, dist_save):
        self.logger.info("Picture named %s save at %s"%(name_save, dist_save))
    
    def log_mouse_position(self, position):
        self.logger.info("Coordonnées de la souris : %s"%position)
    
    def log_step(self):
        # case error
        self.logger.error("Step can't be fix at a value < 0")
    
    def log_port_connection(self, port):
        # case sucess vs failed
        print("wait")
    
    def log_camera_connection(self, camera):
        # case sucess vs failed
        print("wait")
