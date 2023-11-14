"""PROGRAMME CONNEx²CTIQUE DU LASER"""

import cv2
from serial import Serial
import numpy as np
import sys

logger_path = sys.path[0].replace('LASER', 'LOGGER')
try : 
    sys.path.append(logger_path)
except :
    print("Error during import of path")
from LOGGER.logger import *

# Création d'une connexion série
ser = Serial()

# Définition des dimensions et du pas de maille
mesh_dim = 1
mesh_step = 10

# Initialisation du tableau de mailles
mesh = np.ndarray((mesh_dim, mesh_dim), dtype=dict)

# Mise à jour des dimensions de la maille
def update_dim(dim: str):
    global mesh_dim
    mesh_dim = int(dim)

# Incrément du pas de maille
def step_plus():
    global mesh_step
    mesh_step += 1

# Décrément du pas de maille
def step_less():
    global mesh_step
    mesh_step -= 1
    if mesh_step == 0:
        mesh_step = 1
        print("Le pas de maille ne peut pas être < 0")

# Génération d'une maille ponctuelle
def generate_point_mesh(x: int, y: int):
    global mesh_dim, mesh
    mesh_dim = 1
    mesh = np.ndarray((mesh_dim, mesh_dim), dtype=dict)
    mesh[0][0] = {'x': x, 'y': y, 'is_point': True}

# Génération d'une maille carrée
def generate_square_mesh(x: int, y: int):
    global mesh_dim, mesh_step, mesh
    mesh = np.ndarray((mesh_dim, mesh_dim), dtype=dict)
    for i in range(0, mesh_dim):
        for j in range(0, mesh_dim):
            mesh[i][j] = {'x': x + i*mesh_step, 'y': y + j*mesh_step, 'is_point': True}

# Génération d'une maille circulaire
def generate_circular_mesh(x: int, y: int):
    global mesh_dim, mesh_step, mesh
    radius = int(mesh_dim/2)
    mesh = np.ndarray((mesh_dim, mesh_dim), dtype=dict)

    center_x = (x+radius)-1
    center_y = (y+radius)-1

    for i in range(-radius, radius+1):
        for j in range(-radius, radius+1):
            if ((i)*(i) + (j)*(j) < mesh_dim*mesh_dim/4 - 1):
                mesh[i][j] = {'x': center_x + i*(mesh_step+1), 'y': center_y + j*(mesh_step+1), 'is_point': True}
            else:
                mesh[i][j] = {'x': center_x + i*(mesh_step+1), 'y': center_y + j*(mesh_step+1), 'is_point': False}

# Conversion des coordonnées de la maille de la GUI en mouvements moteurs
def coordinates_to_moves(coordinates: np.ndarray) -> list:
    pass # Manque de temps, à réaliser !

# Connexion à un port série
def port_connection(port: str) -> bool:
    global ser
    try:
        ser = Serial(port, 115200)
        logger.log_port_connection(port, "successful", None)
        # print("Connexion au port : " + port + " réussie.")
    except Exception as e:
        logger.log_port_connection(port, "failed", e)
        # print("Connexion au port : " + port + " échouée...")
        # print(e)
        return False
    return True

# Initialisation de la capture vidéo
def camera_VideoCapture(cam: str):
    return cv2.VideoCapture(cam)

# Connexion à une caméra
def camera_connection(cam: str) -> bool:
    global camera
    try:
        camera = cv2.VideoCapture(cam)
        logger.log_camera_connection(cam, "successful", None)
        # print("Connection to camera : " + str(cam) + " successful.")
    except Exception as e:
        logger.log_camera_connection(cam, "failed", e)
        # print("Connection to camera : " + str(cam) + "  failed...")
        # print(e)
        return False
    return True
