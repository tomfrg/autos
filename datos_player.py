
import os
import json
import pygame


class Datos_player:
    def __init__(self, nombre:str, puntuacion:int, ubicacion:str) -> None:
        self.ubicacion = ubicacion
        self.puntuacion = puntuacion
        self.nombre = nombre
    
    def leer(self):
        with open(self.ubicacion,"r", newline="") as file:
            self.data = json.load(file)
        return self.data
            

    def escribir(self):
        with open(self.ubicacion, 'w') as file:
            json.dump(self.datos, file, indent=2)


    def mostrar_player(self):
        with open(self.ubicacion,"r", newline="") as file:
            self.data = json.load(file)
            for i in self.data:
                nomrbe = i["nombre"]
                puntuacion = i["puntuacion"]
                print(f"{nomrbe} || {puntuacion}")
            
            
    def verificar_json(self):
        # Verificar si el archivo JSON ya existe
        if os.path.exists(self.ubicacion):
            print(f"El archivo JSON ya existe. No se realizarán cambios.")
        else:
            # Crear un nuevo archivo JSON con el contenido inicial si se proporciona
            with open(self.ubicacion, 'w') as file:
                json.dump([], file)
                print(f"Se ha creado un nuevo archivo JSON en '{self.ubicacion}'.")
            
            
    def agregar_o_sumar_puntos(self):
        
        self.verificar_json()
        
        # Cargar el JSON desde el archivo
        with open(self.ubicacion, 'r+') as f:
            self.datos = json.load(f)

        # Buscar el usuario en los datos
        usuario_existente = next((usuario for usuario in self.datos if usuario['nombre'] == self.nombre), None)

        if usuario_existente:
            # El usuario ya existe, sumar la puntuación
            usuario_existente['puntuacion'] += self.puntuacion
            print(f"Puntos agregados a {self.nombre}. Puntuación total: {usuario_existente['puntuacion']}")
        else:
            # Agregar un nuevo usuario al JSON
            nuevo_usuario = {'nombre': self.nombre, 'puntuacion': self.puntuacion}
            self.datos.append(nuevo_usuario)
            print(f"Nuevo usuario agregado: {self.nombre} con puntuación {self.puntuacion}")
            
    def mostrar_en_pantalla(self):
        pygame.init()

        pantalla = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("Contenido del JSON")
        
        