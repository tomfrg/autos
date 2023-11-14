import pygame
from objetos import *
from funciones import *
from constantes import *
from personaje import *
from datos_player import *

pygame.init()

ubicacion_json = "GAME_PY\player_datos.json"
puntuacion = 0

pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("autos")


imagen_auto = declarar_imagenes("GAME_PY/photos_car/Car.png")
imagen_enemigo = declarar_imagenes("GAME_PY/photos_car/Car_malo.png")
imagen_enemigo_police = declarar_imagenes("GAME_PY/photos_car/Car_police.png")
imagen_fondo_menu = declarar_imagenes("GAME_PY/fondos/background.png")
imagen_fondo_street = declarar_imagenes("GAME_PY/fondos/street.png")
imagen_tutorial = declarar_imagenes("GAME_PY/fondos/tutorial.jpg")

imagen_tutorial = pygame.transform.scale(imagen_tutorial, (ANCHO_VENTANA - 100, ALTO_VENTANA - 150))
imagen_tutorial_rect = imagen_tutorial.get_rect()
imagen_tutorial_rect.center = (ANCHO_VENTANA // 2, ALTO_VENTANA // 2)

texto_ingreso_explicativo = "Ingrese nombre y disfrute ;)   (presionar [ENTER] para confirmar)"

texto_ingreso_usuario = Texto(pantalla, COLOR_BLANCO, None, texto_ingreso_explicativo, 400, 180, 25)
score = Texto(pantalla, COLOR_NEGRO, None, "SCORE : " + str(puntuacion), 60, 20, 35)
puntuacion_texto = Texto(pantalla, COLOR_NEGRO, None, str(puntuacion), 400, (95 * 4), 40)
victoria_txt = Texto(pantalla, COLOR_VERDE, None, "VICTORIA", 400, 260, 40)
game_over_txt = Texto(pantalla, COLOR_ROJO, None, "GAME OVER", 400, 260, 40)


RELOJ = pygame.time.Clock()
movimiento_enemigo = -100
movimiento_enemigo_police = 700
y = 0

# Estado del juego (banderas que ejecuta en bucle secciones del juego)
estado_juego = {
    'run_menu': False,
    'run_game': False,
    'run_tutorial': False,
    'end_game': False,
    'run_victory': False,
    'player_insert': True,
    'game_over': False,
    'flag_vivo': True,
    'colision_point': True,
    'salir': False,
}

salir = False
nombre_player = None

play_boton = Botton(pantalla, "EMPEZAR", 350, 95)
salir_boton = Botton(pantalla, "SALIR", 350, (95 * 4))
tutorial_boton = Botton(pantalla, "TUTORIAL", 350, (95 * 2))
ir_menu_boton = Botton(pantalla, "Ir al Menu", 350, 550)

input_box = InputBox(300, 300, 140, 32)


#  ---RUN GAME---

while True:
    lista_eventos = pygame.event.get()
    for evento in lista_eventos:
        if evento.type == pygame.QUIT or estado_juego['salir']:
            print(puntuacion)
            datos = Datos_player(nombre_player,puntuacion,"GAME_PY\player_datos.json")

            datos.agregar_o_sumar_puntos()
            datos.escribir()
            
            pygame.quit()
            exit()

        if evento.type == pygame.MOUSEBUTTONDOWN:
            posicion_click = list(evento.pos)
            print(posicion_click)

            play_boton_bool = play_boton.checar_colision(posicion_click, play_boton.rect)
            salir_boton_bool = play_boton.checar_colision(posicion_click, salir_boton.rect)
            ir_menu_boton_bool = play_boton.checar_colision(posicion_click, ir_menu_boton.rect)
            tutorial_boton_bool = play_boton.checar_colision(posicion_click, tutorial_boton.rect)


    #   FONDO DE PANTALLA
    if estado_juego['run_menu'] or estado_juego['player_insert'] or estado_juego['end_game'] or estado_juego['run_tutorial']:
        pantalla.blit(imagen_fondo_menu, (0, 0))
    else:
        fondo = Fondo(y, imagen_fondo_street, pantalla)
        fondo.ejecutar_fondo()
        y += 4
        

    #   --------------------------------------------------------INGRESAR JUGADOR-------------------------------------------------------
    if estado_juego['player_insert']:
        #texto_ingreso_usuario.declarar_texto()
        texto_ingreso_usuario.mostrar_texto()
        
        for evento in lista_eventos:
            nombre_player = input_box.manejar_evento(evento)
        input_box.dibujar(pantalla)

        if nombre_player != None:
            estado_juego['player_insert'] = False
            estado_juego['run_menu'] = True
            nombre_player = input_box.texto


    #   --------------------------------------------------------MENU-------------------------------------------------------
    if estado_juego['run_menu']:
        play_boton.dibujar_boton()
        salir_boton.dibujar_boton()
        tutorial_boton.dibujar_boton()

        if play_boton_bool:  # EMPEZAR
            player = Player(pantalla, COLOR_AMARILLO, auto_y, auto_x, 60, 100, imagen_auto)
            estado_juego['run_game'] = True
            estado_juego['run_menu'] = False
            tamaño_barra = 0

        if salir_boton_bool:  # SALIR
            estado_juego['salir'] = True
            
        if tutorial_boton_bool:  # SALIR
            estado_juego['run_tutorial'] = True
            estado_juego['run_menu'] = False
            

    #   TUTORIAL
    if estado_juego['run_tutorial']:
        pantalla.blit(imagen_tutorial, imagen_tutorial_rect)
        ir_menu_boton.dibujar_boton()
        if ir_menu_boton_bool:
            estado_juego['run_tutorial'] = False
            estado_juego['run_menu'] = True

    #   --------------------------------------------------------JUEGO-------------------------------------------------------
    if estado_juego['run_game']:
        
        score.texto = "SCORE: " + str(puntuacion)
        score.actualizar_texto()
        
        # ENEMIGO
        if movimiento_enemigo <= -100:
            coord_generar_auto1 = generar_numero_random(102, 640)
        if movimiento_enemigo_police >= 600:
            coord_generar_auto2 = generar_numero_random(102, 640)

        enemigo = Enemigos(pantalla, COLOR_ROJO, coord_generar_auto1, movimiento_enemigo, 60, 100, imagen_enemigo)
        enemigo_police = Enemigos(pantalla, COLOR_ROJO, coord_generar_auto2, movimiento_enemigo_police, 60, 100,imagen_enemigo_police)
                                  
        # generar y mover auto malo
        if movimiento_enemigo < 600:
            rect_enemigo = enemigo.crear_auto_malo()
            movimiento_enemigo = enemigo.mover_auto_malo(7)
        else:  # auto malo sale de la pantalla y desaparece
            movimiento_enemigo = -100

        if movimiento_enemigo_police > -100:
            rect_enemigo_police = enemigo_police.crear_auto_malo()
            movimiento_enemigo_police = enemigo_police.mover_auto_malo(-4)
        else:
            movimiento_enemigo_police = 600

        # AUTO (player)
        if estado_juego['flag_vivo']:
            player.updates()
            player.movimiento()
            rect_auto = player.hitbox()

            # colision
            colision_enemigo_01 = comprobar_colision(rect_enemigo, rect_auto)
            colision_enemigo_02 = comprobar_colision(rect_enemigo_police, rect_auto)
            if colision_enemigo_01 or colision_enemigo_02:
                coord_generar_auto1 = 1000
                coord_generar_auto2 = 1000
                estado_juego['game_over'] = True
                estado_juego['run_game'] = False
                estado_juego['end_game'] = True

        # POINTS
        point = Point(pantalla, COLOR_VERDE, 10)
        if estado_juego['colision_point']:
            point_x = generar_numero_random(150, 500)
            point_y = generar_numero_random(50, 500)
        circle_point = point.generar_point(point_x, point_y)
        estado_juego['colision_point'] = comprobar_colision(circle_point, rect_auto)
        puntuacion = point.sumar_point(estado_juego['colision_point'], puntuacion)

        # SCORE
        score.mostrar_texto()
        
        # barra de progreso
        if estado_juego['flag_vivo']:
            pygame.draw.rect(pantalla, COLOR_CELESTE, (30, 550, 200, 30))
            barra_progreso = Barra_progreso(pantalla, COLOR_ROJO, 30, 550, tamaño_barra, 30)
            tamaño_barra = barra_progreso.aumentar_barra()
            barra_progreso.generar_barra(tamaño_barra)
            
            # VICTORIA
            if tamaño_barra > 200:
                estado_juego['run_game'] = False
                estado_juego['run_victory'] = True
                estado_juego['end_game'] = True


    #   --------------------------------------------------------end_game-------------------------------------------------------
    if estado_juego['end_game']:
        puntuacion_texto.texto = str(puntuacion)
        puntuacion_texto.actualizar_texto()
        if estado_juego['run_victory']:  # victoria
            
            puntuacion_texto.mostrar_texto()
            victoria_txt.mostrar_texto()

        if estado_juego['game_over']:
            puntuacion_texto.mostrar_texto()
            game_over_txt.mostrar_texto()

        ir_menu_boton.dibujar_boton()
        if ir_menu_boton_bool:
            estado_juego['run_menu'] = True
            estado_juego['end_game'] = False
            estado_juego['game_over'] = False
            estado_juego['run_victory'] = False
            estado_juego['run_game'] = False

    RELOJ.tick(FPS)
    pygame.display.flip()
    

