import random
import pygame
from constantes import*


def generar_numero_random(range_a:int ,range_b:int) -> int:
    numer_random = random.randint(range_a,range_b)
    
    return numer_random



def comprobar_colision(colisionado_1,colisionado_2) -> bool:
    if colisionado_2.colliderect(colisionado_1):
        colision = True
    else:
        colision = False
    return colision


def declarar_imagenes(ubicacion):
    imagen = pygame.image.load(ubicacion)
    return imagen

