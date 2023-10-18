"""PROGRAMME PRINCIPAL DU LASER"""

from PyQt5 import QtCore, QtGui, QtWidgets
import IHM_Laser as IHM
from IHM_Laser import *

#lien du répertoire des images
image_directory = "Images/"
n=0
class Main(QMainWindow):
    def __init__(self): # Constructeur de classe
        QMainWindow.__init__(self) # Appel du constructeur de la classe parent
        self.ui = IHM.LaserUI() # Initialisation de l'IHM de la classe LaserUI
        self.ui.setupUi(self) # Configuration de l'interface utilisateur
        # Configuration des boutons de l'interface utilisateur pour qu'ils exécutent des fonctions lorsqu'ils sont cliqués
        self.ui.device_co_connect.clicked.connect(self.connection_device)
        self.ui.device_co_refresh.clicked.connect(self.list_ports_device)
        self.ui.camera_co_connect.clicked.connect(self.connection_camera)
        self.ui.camera_co_refresh.clicked.connect(self.list_ports_camera)
        self.ui.device_aqcisition.clicked.connect(self.get_device_info)
        self.ui.control_button.clicked.connect(self.handle_beam)
        self.ui.clear_button.clicked.connect(self.clearing_points)
    
        # Configuration des timers
        print("Main.init: Setting up timers...")
        QTimer.singleShot(100, self.update_background)
        QTimer.singleShot(250, self.update_progress_bar)
        QTimer.singleShot(10000, self.save_current_state)

    # Méthode pour obtenir les informations sur le dispositif
    def get_device_info(self):
    # Si le contrôleur est connecté
        if self.ui.controller_connected:
            # Envoie de commandes au port série pour obtenir les informations
            Laser.ser.write('GetDevInfo,Controller,0,Name\n'.encode())
            name = Laser.ser.readline().decode('ascii','replace')
            print(name)
            Laser.ser.write('GetDevInfo,Controller,0,Version\n'.encode())
            vers = Laser.ser.readline().decode('ascii','replace')
            print(vers)
            Laser.ser.write('GetDevInfo,SensorHead,0,Name\n'.encode())
            nameSH = Laser.ser.readline().decode('ascii','replace')
            print(nameSH)
            Laser.ser.write('GetDevInfo,SensorHead,0,Version\n'.encode())
            versSH = Laser.ser.readline().decode('ascii','replace')
            print(versSH)
            # Mise à jour de l'interface utilisateur avec les informations obtenues
            self.ui.device_info_l.setText("\nControler:\n"+ name + vers +"Laser:\n"+ nameSH + versSH)

    # Méthode pour lister les ports disponibles pour le dispositif
    def list_ports_device(self):
        # Récupération des ports série disponibles
        ports = serial.tools.list_ports.comports()
        # Effacement de la liste des ports de l'interface utilisateur
        self.ui.device_co_listbox.clear()
        # Si des ports sont disponibles
        if (len(ports) != 0):
            devices = []
            # Pour chaque port disponible, ajout à la liste des ports de l'interface utilisateur
            for p in ports:
                self.ui.device_co_listbox.addItem(p.device)
        else:
            self.ui.device_co_listbox.addItem("No device found")

    # Méthode pour établir une connexion avec le dispositif
    def connection_device(self):
        # Récupération du port sélectionné dans l'interface utilisateur
        port = str(self.ui.device_co_listbox.currentItem().text())
        # Si un port est sélectionné
        if (port):
            # Tentative de connexion au port
            self.ui.controller_connected = Laser.port_connection(port)

    # Méthode pour lister les caméras disponibles
    def list_ports_camera(self):
        index = 0
        arr = []
        i = 5
        # Effacer la liste déroulante
        self.ui.camera_co_listbox.clear()
        while i > 0:
            # Ouvrir une capture vidéo à partir de l'index actuel
            cap = cv2.VideoCapture(index)
            # Vérifier si la capture vidéo a réussi
            if cap.read()[0]:
                # Ajouter l'index de la caméra dans le tableau
                arr.append(index)
                # Créer un nom de périphérique pour la caméra en fonction du système d'exploitation
                device = str(index)
                # Ajouter le nom de périphérique à la liste déroulante
                self.ui.camera_co_listbox.addItem(device)
                cap.release()
            index += 1
            i -= 1
        # Si aucune caméra n'a été trouvée, afficher un message approprié dans la liste déroulante
        if (len(arr)==0):
            self.ui.camera_co_listbox.addItem("No device found")

    # Méthode pour établir une connexion à la caméra sélectionnée dans la liste déroulante camera_co_listbox
    def connection_camera(self):
        # Récupérer le nom de la caméra sélectionnée dans la liste déroulante
        self.ui.cam = str(self.ui.camera_co_listbox.currentItem().text())
        if (self.ui.cam):
            # Etablir la connexion à la caméra en utilisant le nom de la caméra
            self.ui.camera_connected = Laser.camera_connection(self.ui.cam)

    # Méthode pour sauvegarder l'état actuel du système
    def save_current_state(self):
        #sauvegarde de l'image
        global n
        if (self.ui.camera_connected):#SI la caméra est connectée
            if not os.path.exists(image_directory):#si le dossier n'existe pas
                os.makedirs(image_directory)#on le crée
            self.read_camera().save(image_directory+str(n)+".png")
            n+=1
        else:
            print("Main.save_current_state: No camera connected...")
        QTimer.singleShot(1000, self.save_current_state)

    # Méthode pour lire le flux vidéo de la caméra connectée
    def read_camera(self):
        if (self.ui.camera_connected):
            # Créer un objet de capture vidéo à partir de l'index de la caméra
            camera = Laser.camera_VideoCapture(int(self.ui.cam))
            #print("La camera read 1 {} camera read 0 {}".format(camera.read()[0],camera.read()))
            # Lire l'image du flux vidéo et la convertir en image RGB
            cv2image = cv2.cvtColor(camera.read()[1], cv2.COLOR_BGR2RGB)
            # Redimensionner l'image en 400 x 315 pixels
            img = cv2.resize(cv2image, (400, 315))
            # Convertir l'image en format QPixmap pour affichage dans l'interface utilisateur
            return self.convert_cv_qt(img)
        else:
            return None 

    # Méthode pour convertir une image OpenCV en un format compatible avec l'affichage dans l'interface utilisateur
    def convert_cv_qt(self, cv_img):
        # Convertir l'image en RGB
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        # Récupérer les dimensions de l'image
        h, w, ch = rgb_image.shape
        # Calculer le nombre de bytes par ligne de l'image
        bytes_per_line = ch * w
        # Convertir l'image en format QImage
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        # Redimensionner l'image pour l'affichage
        p = convert_to_Qt_format.scaled(400, 315, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    # Méthode pour mettre à jour l'image de fond de l'interface utilisateur
    def update_background(self):
        if (self.ui.camera_connected): # Si la caméra est connectée
            self.ui.camera_return.setPixmap(self.read_camera()) # Mettre à jour l'image de la caméra
        else:
            self.ui.camera_return.setStyleSheet("background-color: black;") # Sinon, mettre un fond noir
        QTimer.singleShot(100, self.update_background) # Programmer une nouvelle exécution de la fonction après 100 ms

    # Méthode pour gérer l'état du faisceau laser
    def handle_beam(self):
        if self.ui.controller_connected: # Si le laser est connecté
            Laser.ser.write('Get,SensorHead,0,Laser\n'.encode()) # Envoyer une commande pour récupérer l'état du faisceau laser
            actif = Laser.ser.readline().decode('ascii','replace') # Lire la réponse du laser
            if(actif == "0\n"): # Si le faisceau est éteint
                self.ui.control_button.setText("Off") # Mettre à jour le texte du bouton
                self.ui.control_pan.setStyleSheet("background-color: lime;") # Mettre à jour la couleur de fond de la zone de contrôle
                Laser.ser.write('Set,SensorHead,0,Laser,1\n'.encode()) # Envoyer une commande pour allumer le faisceau laser
            if(actif== "1\n"): # Si le faisceau est allumé
                self.ui.control_button.setText("On") # Mettre à jour le texte du bouton
                self.ui.control_pan.setStyleSheet("background-color: pink;") # Mettre à jour la couleur de fond de la zone de contrôle
                Laser.ser.write('Set,SensorHead,0,Laser,0\n'.encode()) # Envoyer une commande pour éteindre le faisceau laser
        else:
            print("ControlFrame.handle_beam: No controller connected...") # Afficher un message d'erreur si le laser n'est pas connecté

    # Méthode pour mettre à jour la barre de progression de la puissance du laser
    def update_progress_bar(self):
        if self.ui.controller_connected: # Si le laser est connecté
            Laser.ser.write('Get,SignalLevel,0,Value\n'.encode()) # Envoie une commande pour récupérer la puissance du laser
            actif = Laser.ser.readline().decode('ascii','replace') # Lire la réponse du laser
            #print("retour laser = " + actif)
            self.ui.signal_bar.setValue(int(float(actif)/775*100)) # Mettre à jour la barre de progression et convertir la valeur en pourcentage
        QTimer.singleShot(250, self.update_progress_bar)# Programmer une nouvelle exécution de la fonction après 250 ms
     #Récupère les coordonnées de la souris (x et y)

    #La def pour clear:
    def clearing_points (self):
        self.ui.camera_return.vider()



# Vérifier que ce fichier est le fichier principal qui est exécuté
if __name__ == "__main__":
    # Créer une instance de QApplication
    app = QtWidgets.QApplication(sys.argv)
    # Créer une instance de la classe Main
    MainWindow = Main()
    # Afficher la fenêtre principale
    MainWindow.show()
    # Lancer la boucle principale de l'application jusqu'à sa fermeture
    sys.exit(app.exec_())