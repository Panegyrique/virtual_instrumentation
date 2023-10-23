"""PROGRAMME INTERFACE DU LASER"""

import sys
from PyQt5.QtWidgets import QProgressBar, QGridLayout, QListWidget, QMessageBox, QFrame, QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QComboBox, QSlider
from PyQt5.QtCore import Qt, QRegExp, QRect, QTimer, QPoint
from PyQt5.QtGui import QDoubleValidator, QRegExpValidator, QPalette, QFont, QImage, QPixmap, QPen, QPainter, QBrush
from serial import Serial
import serial.tools.list_ports
import cv2
import Laser
import os
from logger import *


# Définition d'une classe ImageLabel qui hérite de la classe QLabel
class ImageLabel(QLabel):
    # Constructeur de la classe ImageLabel prenant en paramètre un parent (par défaut None)
    def __init__(self, parent=None):
        # Appel du constructeur de la classe QLabel
        super().__init__(parent)
        # Active le suivi de la souris
        self.setMouseTracking(True)
        # Initialise les coordonnées à None et la liste de points à vide
        self.coordinates = None
        self.points = []

    # Méthode pour vider la liste de points et effacer le contenu de l'image
    def vider(self):
        # Efface la liste de points
        self.points.clear()
        # Crée une pixmap de la taille de l'image courante et la remplit de transparence
        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.transparent)
        # Initialise un painter avec la pixmap
        painter = QPainter(pixmap)
        # Met à jour l'affichage de l'image
        self.update
        # Termine le dessin
        painter.end()
        # Définit la pixmap comme l'image de l'étiquette
        self.setPixmap(pixmap)

    # Méthode appelée lorsque la souris se déplace sur l'image
    def mouseMoveEvent(self, event):
        # Récupère les coordonnées de la souris
        x = event.x()
        y = event.y()
        # Stocke les coordonnées de la souris dans l'attribut "mouse_pos"
        self.mouse_pos = QPoint(x, y)
        # Met à jour l'affichage de l'image
        self.update()

    # Méthode appelée lorsqu'un bouton de la souris est enfoncé sur l'image
    def mousePressEvent(self, event):
        # Récupère les coordonnées de la souris
        x = event.x()
        y = event.y()
        # Stocke les coordonnées de la souris dans l'attribut "mouse_pos"
        self.mouse_pos = QPoint(x, y)
        # Crée une pixmap de la taille de l'image courante et la remplit de transparence
        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.transparent)
        # Initialise un painter avec la pixmap
        painter = QPainter(pixmap)
        # Définit la taille de la croix
        cross_size = 10

        # Si le bouton enfoncé est le bouton gauche de la souris
        if event.button() == Qt.LeftButton:
            # Stocke les coordonnées de la souris dans l'attribut "coordinates" et les ajoute à la liste "points"
            self.coordinates=(self.mouse_pos.x(),self.mouse_pos.y())
            logger.log_mouse_position(self.coordinates)
            # print("Coordonnées de la souris :", self.coordinates)
            
            self.points.append(self.coordinates)
            # Définit la couleur et l'épaisseur du stylo utilisé pour dessiner la croix
            pen = QPen(Qt.red, 2, Qt.SolidLine)
            # Définit la couleur de la brosse utilisée pour remplir la croix
            brush = QBrush(Qt.SolidPattern)
            # Dessine une croix pour chaque point dans la liste "points"
            for point in self.points:
                # Calcule les coordonnées du coin supérieur gauche de la croix
                x = point[0] - cross_size/2
                y = point[1] - cross_size/2
                # Dessine la croix
                painter.setPen(pen)
                painter.setBrush(brush)
                painter.drawLine(int(round(x)), int(round(y)), int(round(x+cross_size)), int(round(y+cross_size)))
                painter.drawLine(int(round(x)), int(round(y+cross_size)), int(round(x+cross_size)), int(round(y)))
            self.update
            painter.end()
            self.setPixmap(pixmap)      
 
# Définition d'une classe pour l'interface utilisateur                    
class LaserUI(object):
    def setupUi(self, MainWindow):
        super().__init__()
        # Définition des propriétés de la fenêtre
        self.title = 'Laser Controller'
        self.left = 10
        self.top = 50
        self.width = 400
        self.height = 860
        self.cam = ""

        # Définition du titre de la fenêtre et de sa taille
        MainWindow.setWindowTitle(self.title)
        MainWindow.setGeometry(self.left, self.top, self.width, self.height)
        self.controller_connected = False
        self.camera_connected = False
        self.setMouseTracking = True

        # Création des widgets pour la connexion de l'appareil
        self.device_co_pan = QLabel(MainWindow)
        self.device_co_pan.move(0, 0)
        self.device_co_pan.resize(200, 110)
        self.device_co_pan.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.device_co_pan.setLineWidth(1)

        self.device_co_title = QLabel("Device connection", MainWindow)
        self.device_co_title.setFont(QFont('Arial', 8,))
        self.device_co_title.move(0, 5)
        self.device_co_title.resize(200, 20)
        self.device_co_title.setAlignment(Qt.AlignCenter)

        self.device_co_listbox = QListWidget(MainWindow)
        self.device_co_listbox.setFont(QFont('Arial', 5,)) 
        self.device_co_listbox.resize(180, 40)
        self.device_co_listbox.move(10,30)

        self.device_co_refresh = QPushButton("Refresh", MainWindow)
        self.device_co_refresh.setFont(QFont('Arial', 7)) 
        self.device_co_refresh.resize(90, 30)
        self.device_co_refresh.move(10,70)

        self.device_co_connect = QPushButton("Connect", MainWindow)
        self.device_co_connect.setFont(QFont('Arial', 7)) 
        self.device_co_connect.resize(90, 30)
        self.device_co_connect.move(100,70)

        # Création des widgets pour la connexion de la caméra
        self.camera_co_pan = QLabel(MainWindow)
        self.camera_co_pan.move(200, 0)
        self.camera_co_pan.resize(200, 110)
        self.camera_co_pan.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.camera_co_pan.setLineWidth(1)

        self.camera_co_title = QLabel("Camera connection", MainWindow)
        self.camera_co_title.setFont(QFont('Arial', 8)) 
        self.camera_co_title.move(200, 5)
        self.camera_co_title.resize(200, 20)
        self.camera_co_title.setAlignment(Qt.AlignCenter)

        self.camera_co_listbox = QListWidget(MainWindow)
        self.camera_co_listbox.setFont(QFont('Arial', 5,)) 
        self.camera_co_listbox.resize(180, 40)
        self.camera_co_listbox.move(210,30)

        self.camera_co_refresh = QPushButton("Refresh", MainWindow)
        self.camera_co_refresh.setFont(QFont('Arial', 7)) 
        self.camera_co_refresh.resize(90, 30)
        self.camera_co_refresh.move(210,70)

        self.camera_co_connect = QPushButton("Connect", MainWindow)
        self.camera_co_connect.setFont(QFont('Arial', 7)) 
        self.camera_co_connect.resize(90, 30)
        self.camera_co_connect.move(300,70)

        self.camera_co_pan = QLabel(MainWindow)
        self.camera_co_pan.move(0, 110)
        self.camera_co_pan.resize(400, 400)
        self.camera_co_pan.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.camera_co_pan.setLineWidth(1)
        
        self.clear_button = QPushButton("Clear", MainWindow)
        self.clear_button.setFont(QFont('Arial', 7)) 
        self.clear_button.resize(200, 30)
        self.clear_button.move(200,155)

        self.camera_return = ImageLabel(MainWindow)
        self.camera_return.move(0, 190)
        self.camera_return.resize(400, 315)

        self.camera_title = QLabel("Camera", MainWindow)
        self.camera_title.setFont(QFont('Arial', 8)) 
        self.camera_title.move(0, 115)
        self.camera_title.resize(400, 20)
        self.camera_title.setAlignment(Qt.AlignCenter)

        self.camera_mesh = QLabel("Mesh Patern", MainWindow)
        self.camera_mesh.setFont(QFont('Arial', 7)) 
        self.camera_mesh.move(0, 135)
        self.camera_mesh.resize(400, 20)
        self.camera_mesh.setAlignment(Qt.AlignCenter)

        self.camera_mesh_box = QComboBox(MainWindow)
        self.camera_mesh_box.addItems(['Point', 'Square', 'Circle'])
        self.camera_mesh_box.setFont(QFont('Arial', 7)) 
        self.camera_mesh_box.move(0, 155)
        self.camera_mesh_box.resize(200, 30)

        # Création des widgets pour la fenêtre et le bouton de contrôle
        self.control_pan = QLabel(MainWindow)
        self.control_pan.move(0, 510)
        self.control_pan.resize(400, 65)
        self.control_pan.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.control_pan.setLineWidth(1)
        self.control_pan.setStyleSheet("background-color: pink;")

        self.control_title = QLabel("Control", MainWindow)
        self.control_title.setFont(QFont('Arial', 8)) 
        self.control_title.move(0, 515)
        self.control_title.resize(400, 20)
        self.control_title.setAlignment(Qt.AlignCenter)

        self.control_button = QPushButton("On", MainWindow)
        self.control_button.setFont(QFont('Arial', 7)) 
        self.control_button.resize(180, 30)
        self.control_button.move(110,540)

        # Création des widgets pour le signal retourné par le laser
        self.signal_pan = QLabel(MainWindow)
        self.signal_pan.move(0, 575)
        self.signal_pan.resize(400, 60)
        self.signal_pan.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.signal_pan.setLineWidth(1)

        self.signal_title = QLabel("Signal", MainWindow)
        self.signal_title.setFont(QFont('Arial', 8)) 
        self.signal_title.move(0, 580)
        self.signal_title.resize(400, 25)
        self.signal_title.setAlignment(Qt.AlignCenter)

        self.signal_bar = QProgressBar(MainWindow, minimum=0, maximum=100)
        self.signal_bar.move(10, 600)
        self.signal_bar.resize(380, 30)

        self.info_pan = QLabel(MainWindow)
        self.info_pan.move(0, 635)
        self.info_pan.resize(400, 225)
        self.info_pan.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.info_pan.setLineWidth(1)

        # Création des widgets pour le retour des informations de l'appareil connecté
        self.device_info_title = QLabel("Device Info", MainWindow)
        self.device_info_title.setFont(QFont('Arial', 8)) 
        self.device_info_title.move(0, 640)
        self.device_info_title.resize(400, 20)
        self.device_info_title.setAlignment(Qt.AlignCenter)

        self.device_info = QPushButton("Dev info", MainWindow)
        self.device_info.setFont(QFont('Arial', 7)) 
        self.device_info.resize(180, 30)
        self.device_info.move(110,665)

        self.device_info_l = QLabel("Controler:\nUndefined\nUndefined\nLaser:\nUndefined\nUndefined", MainWindow)
        self.device_info_l.setFont(QFont('Arial', 8)) 
        self.device_info_l.move(0, 680)
        self.device_info_l.resize(400, 180)
        self.device_info_l.setAlignment(Qt.AlignCenter)

        # Création des widgets pour le retour des informations pour l'acquisition
        self.device_acquisition = QPushButton("Acquisition", MainWindow)
        self.device_acquisition.setFont(QFont('Arial', 7)) 
        self.device_acquisition.resize(180, 30)
        self.device_acquisition.move(110,825)
                    
if __name__ == "__main__":
    # Création d'une instance de l'application Qt
    app = QApplication(sys.argv)
    # Création d'une instance de la fenêtre principale
    MainWindow = QMainWindow()
    # Création d'une instance de l'interface utilisateur
    ui = LaserUI()
    # Configuration de l'interface utilisateur pour la fenêtre principale
    ui.setupUi(MainWindow)
    # Affichage de la fenêtre principale
    MainWindow.show()
    # Exécution de la boucle principale de l'application
    sys.exit(app.exec_())
    
    