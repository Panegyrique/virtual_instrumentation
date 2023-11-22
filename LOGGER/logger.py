import logging
import os

class Log():

    def __init__(self):
        file_path = '../app.log'
        if os.path.exists(file_path):
            os.remove(file_path)
        log_directory = os.path.dirname(os.path.abspath(file_path))
        os.chdir(log_directory)
        logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        logging.info('Init log file')
        self.logger = logging.getLogger(__name__)

    def log_controller_state(self, state):
        if not state:
            self.logger.error("ControlFrame.handle_beam: No controller connected...")

#######################
#
#   LASER / CAMERA
#
#######################

    def log_laser_connect(self):
        self.logger.info("Laser is now connected")

    def log_laser_disconnect(self):
        self.logger.info("Laser is now disconnected")

    def log_viewmeter_acquisition(self, value):
        self.logger.info("Viewmeter acquisition at %s"%(str(value)) + "%")
    
    def log_mouse_position(self, position):
        self.logger.info("Coordonnées de la souris : %s"%str(position))
    
    def log_port_connection(self, port, state, exception):
        if state == "failed":
            self.logger.error("Connection to port %s %s, Exception : %s "%(str(port), state, str(exception)))
        else:
            self.logger.info("Connection to port %s %s "%(str(port), state))

    def log_camera_connection(self, cam, state, exception):
        if state == "failed":
            self.logger.error("Connection to camera %s %s, Exception : %s "%(str(cam), state, str(exception)))
        else:
            self.logger.info("Connection to camera %s %s "%(str(cam), state))
    
    def log_camera_acquisition(self):
        self.logger.info("Acquisition of camera")
    
    def log_camera_save(self, state, image_directory, n):
        if not state:
            self.logger.error("Main.save_current_state: No camera connected...")
        else:
            self.logger.info("Image save at : %s as a .png, acquisition n°%s"%(str(image_directory), str(n)))

    def log_device_info(self, name, vers, nameSH, versSH):
        self.logger.info("Controler: %s %s, Laser: %s %s"%(str(name), str(vers), str(nameSH), str(versSH)))

#######################
#
#   MOTORS
#
#######################

    def log_motors_connect(self):
        self.logger.info("Motors are now connected")

    def log_motors_disconnect(self):
        self.logger.info("Motors are now disconnected")

    def log_motors_initiated(self):
        self.logger.info("Motors are now initiated")

    def log_motors_move_forward(self,axis,step):
        self.logger.info("Axis %s is moving forward by %s mm"%(str(axis),str(step)))
    
    def log_motors_move_backward(self,axis,step):
        self.logger.info("Axis %s is moving backward by %s mm"%(str(axis),str(step)))

    def log_motors_position(self,x,y,z):
        self.logger.info("Motors position is x: %s, y: %s, z: %s "%(str(x),str(y),str(z)))


# Permet de ne construire qu'une fois Log() notamment pour le fichier app.log
# Il suffit simplement d'importer logger.py pour pouvoir utiliser la variable sans avoir à construire un nouveau Log()
write_log = Log()