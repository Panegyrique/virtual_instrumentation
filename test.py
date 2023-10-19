from logger import *

monlog = Log()

monlog.log_laser_connect()
monlog.log_laser_disconnect()
monlog.log_viewmeter_value(42)
monlog.log_take_picture("image.jpg", "/path/to/save")
