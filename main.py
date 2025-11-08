import pygame
from genoma import Genoma
from brain import Brain
from dino import Dino
from enemy import Enemy

num_entradas = 3
num_ocultas = 5

screen = pygame.display.set_mode((800, 600))
gen = Genoma(n_entradas=num_entradas, n_ocultas=num_ocultas)
brain = Brain(n_entradas=num_entradas, n_ocultas=num_ocultas)
brain.asignar_pesos(gen.genes)
dino1 = Dino(cerebro=brain)
enemy1 = Enemy()
clock = pygame.time.Clock()

pygame.init()

interruptor = True
while interruptor == True:
        dt = clock.tick(60) / 1000  # tiempo desde último frame

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                interruptor = False

        # ---------------- DECISION AUTOMATICA ----------------
        # calcular el estado para la red
        # por ejemplo:
        distancia_obstaculo = enemy1.x_pos - dino1.x_pos
        altura_obstaculo = enemy1.obj_height
        velocidad = 1.0  # o la velocidad del juego

        estado = [distancia_obstaculo, altura_obstaculo, velocidad]
        accion = dino1.pensar(estado)

        if accion == 1:
            dino1.jump()
        elif accion == 2:
            dino1.crouch()
        else:
            dino1.stop_crouch()
        # ------------------------------------------------------

        # ACTUALIZAR SALTO
        if dino1.jumping():
            dino1.update_jump()

        dino1.update_animation(dt)

        # COLISION
        if dino1.esta_colisionando(enemy1):
            dino1.die()

        # DIBUJAR
        screen.fill((247, 247, 247))
        dino1.draw(screen)
        enemy1.draw(screen)
        enemy1.update()

        pygame.display.flip()


    # # LECTURA DE TECLAS
    # keys = pygame.key.get_pressed()

    # # SALTO / AGACHARSE con teclado
    # if keys[pygame.K_UP]:
    #     dino1.jump()
    # elif keys[pygame.K_DOWN]:
    #     dino1.crouch()
    # else:
    #     dino1.stop_crouch()
