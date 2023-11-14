import pygame
from funciones import*
from constantes import*
from objetos import*


class Player(Rectangulo):
    def __init__(self ,pantalla ,color:int, x:int, y:int, tamaño_x:int, tamaño_y:int,imagen:str) -> None:
        super().__init__(pantalla,color,x,y,tamaño_x,tamaño_y)
        self.imagen = imagen
    
    def hitbox(self):
        rect_player = pygame.Rect(self.x,self.y,self.tamaño_x,self.tamaño_y)
        return rect_player
    
    def movimiento(self) -> None:
        self.imagen = pygame.image.load("GAME_PY/photos_car/Car.png")
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_DOWN]:
            self.y = self.y + VELOCIDAD_AUTO

        if teclas[pygame.K_UP]:
            self.y = self.y - VELOCIDAD_AUTO        

        if teclas[pygame.K_LEFT]:
            self.x = self.x - VELOCIDAD_AUTO
            self.imagen = pygame.image.load("GAME_PY/photos_car/Car_Right.png")

        if teclas[pygame.K_RIGHT]:
            self.x = self.x + VELOCIDAD_AUTO
            self.imagen = pygame.image.load("GAME_PY/photos_car/Car_Left.png") 
             
        self.y = self.y - 1
        
        self.imagen = pygame.transform.scale(self.imagen,(self.tamaño_x,self.tamaño_y))
        rect_player = pygame.Rect(self.x,self.y,self.tamaño_x,self.tamaño_y)
        self.pantalla.blit(self.imagen, rect_player)
        
    def updates(self) -> None:
        if self.x > (ANCHO_VENTANA - 51):
            self.x = (ANCHO_VENTANA - 51)
        
        if self.x < 1:
            self.x = 1
            
        if self.y > (ALTO_VENTANA - 100):
            self.y = (ALTO_VENTANA - 100)
        
        if self.y < 1:
            self.y = 1




class Enemigos(Rectangulo):
    def __init__(self ,pantalla, color:int, x:int, y:int, tamaño_x:int, tamaño_y:int, imagen:str) -> None:
        super().__init__(pantalla,color,x,y,tamaño_x,tamaño_y)
        self.imagen = imagen
        
    def hitbox(self):
        rect_player = pygame.Rect(self.x,self.y,self.tamaño_x,self.tamaño_y)
        return rect_player
       
    def crear_auto_malo(self):
        self.imagen = pygame.transform.scale(self.imagen,(self.tamaño_x,self.tamaño_y))
        rect_enemigo = pygame.Rect(self.x,self.y,self.tamaño_x,self.tamaño_y)
        self.pantalla.blit(self.imagen, rect_enemigo)
        
        return rect_enemigo
        
    def mover_auto_malo(self,velocidad:int) -> int:
        coords_y = self.y + velocidad
        return coords_y
    
    
    
    