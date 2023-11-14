import pygame
from funciones import*
from constantes import*
import sys


class Rectangulo:
    def __init__(self ,pantalla, color:int, x:int, y:int, tamaño_x:int, tamaño_y:int) -> None:
        self.pantalla = pantalla
        self.color = color
        self.x = x
        self.y = y
        self.tamaño_x = tamaño_x
        self.tamaño_y = tamaño_y
        
    def mostrar_rect(self):
        pygame.draw.rect(self.pantalla,self.color,(self.x,self.y,self.tamaño_x,self.tamaño_y))


class Barra_progreso(Rectangulo):
    def __init__(self,pantalla, color:int, x:int, y:int, tamaño_x:int, tamaño_y:int) -> None:
        super().__init__(pantalla,color,x,y,tamaño_x,tamaño_y)

    def generar_barra(self, tamaño_x:int) -> None:
        pygame.draw.rect(self.pantalla,self.color,(self.x,self.y,tamaño_x,self.tamaño_y))
        
    def aumentar_barra(self) -> int:
        if self.tamaño_x < 200:
            tamaño_x = self.tamaño_x + 0.1
        else:
            tamaño_x = 0
        return tamaño_x
    

class Point:
    def __init__(self, pantalla, color:int, radio:int) -> None:
        self.pantalla = pantalla
        self.color = color
        self.radio = radio
    
    def generar_point(self, point_x:int, point_y:int):
        point = pygame.draw.circle(self.pantalla,self.color,(point_x,point_y),self.radio)
        return point

    def sumar_point(self, colision_point:bool, contador_point:int) -> int:
        if colision_point:
            contador_point = contador_point + 3
            print(contador_point) 
        else:
            contador_point = contador_point
        return contador_point       
    
    
class Texto:
    def __init__(self, pantalla, color, fuente, texto, x, y, dimensiones):
        self.pantalla = pantalla
        self.color = color
        self.fuente = fuente
        self.texto = texto
        self.x = x
        self.y = y
        self.dimensiones = dimensiones

        self.actualizar_texto()

    def actualizar_texto(self):
        tipo_texto = pygame.font.Font(self.fuente, self.dimensiones)
        self.superficie = tipo_texto.render(self.texto, True, self.color)
        self.rect = self.superficie.get_rect()
        self.rect.center = (self.x, self.y)

    def mostrar_texto(self):
        self.pantalla.blit(self.superficie, self.rect)

  
class Botton:
    def __init__(self, pantalla, texto:str, x:int, y:int) -> None:
        self.pantalla = pantalla
        self.tamaño_y = 100
        self.tamaño_x = 30
        self.x = x
        self.y = y
        self.color = COLOR_ROJO
        self.texto_color = COLOR_BLANCO
        
        self.font = pygame.font.SysFont(None, 48)
        
        self.rect = pygame.Rect(self.x,self.y, self.tamaño_y, self.tamaño_x)
        self.rect_pos = self.x,self.y
        
        self.prepara_texto(texto)
    
    def prepara_texto(self, texto:str) -> None:
        self.texto_image = self.font.render(texto, True, self.texto_color, self.color)
        self.texto_image_rect = self.texto_image.get_rect()
        self.texto_image_rect.center = self.rect.center
        
    def dibujar_boton(self) -> None:
        self.pantalla.blit(self.texto_image, self.texto_image_rect)    
    
    def checar_colision(self, mouse_pos, play_boton) -> bool:
        if play_boton.collidepoint(mouse_pos):
            retorno = True
        else:
            retorno = False
        return retorno   
    
    
class Victory(Texto):
    def __init__(self, pantalla, color:int, fuente:str, texto:str, x:int , y:int, dimenciones:int) -> None:
        super().__init__(pantalla, color, fuente, texto, x , y, dimenciones)
    
    def pantalla_victory(self) -> None:
        tipo_texto = pygame.font.SysFont(self.fuente,self.dimeciones)
        superficie = tipo_texto.render(self.texto,True,self.color)
        self.pantalla.blit(superficie,(self.y,self.x))
    
    
class GameOver:
    def __init__(self) -> None:
        pass
    
    
class Imagenes:
    def __init__(self,pantalla,imagen,y,x) -> None:
        self.imagen = imagen
        self.y = y
        self.x = x
        self.pantalla = pantalla
        
        self.declarar_imagen()
    
    def declarar_imagen(self):
        self.imagen_diibujada = pygame.image.load(self.imagen)
    
    def dibujar_imagen(self):
        self.pantalla.blit(self.imagen_diibujada,(self.x,self.y))

    
class Fondo:
    def __init__(self,y,imagen_fondo_street,pantalla) -> None:
        self.y = y
        self.imagen_fondo_street = imagen_fondo_street
        self.pantalla = pantalla
    
    def ejecutar_fondo(self):
        y_auxiliar = self.y % self.imagen_fondo_street.get_rect().width
        self.pantalla.blit(self.imagen_fondo_street,(0,y_auxiliar - self.imagen_fondo_street.get_rect().width))
        if y_auxiliar < ALTO_VENTANA:
            self.pantalla.blit(self.imagen_fondo_street,(0,y_auxiliar))   


class InputBox:
    def __init__(self, x, y, ancho, alto, texto=''):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color_inactivo = COLOR_BLANCO
        self.color_activo = COLOR_CELESTE
        self.color = self.color_inactivo
        self.texto = texto
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(texto, True, self.color)
        self.activo = False

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos):
                self.activo = not self.activo
            else:
                self.activo = False
            self.color = self.color_activo if self.activo else self.color_inactivo
            
        if evento.type == pygame.KEYDOWN:
            if self.activo:
                if evento.key == pygame.K_RETURN:
                    nombre_player = self.texto
                    return nombre_player
                
                elif evento.key == pygame.K_BACKSPACE:
                    self.texto = self.texto[:-1]
                    
                else:
                    self.texto += evento.unicode

                self.txt_surface = self.font.render(self.texto, True, COLOR_NEGRO)

    def dibujar(self, pantalla): #da forma al rect
        pygame.draw.rect(pantalla, self.color, self.rect, 0)
        pygame.draw.rect(pantalla, COLOR_NEGRO, self.rect, 2)
        pantalla.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))



