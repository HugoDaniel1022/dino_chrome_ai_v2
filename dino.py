import pygame
import torch
# brain = RandomBrain(input_size=3, hidden_size=5, output_size=1)

# # Ejemplo de entrada
# inputs = np.array([dino_y, enemy_x, enemy_y])
# decision = brain.forward(inputs)

# if decision > 0.5:
#     print("Salta")
# else:
#     print("No salta")



class Dino:
    GROUND_Y = 450
    CROUCH_Y = 484
    WIDTH_NORMAL, HEIGHT_NORMAL = 80, 86
    WIDTH_CROUCH, HEIGHT_CROUCH = 110, 52

    IMAGE_NORMALS = ["images/dino1.png", "images/dino2.png"]
    IMAGE_DUCKS = ["images/duck1.png", "images/duck2.png"]
    IMAGE_JUMP = "images/jump.png"

    def __init__(self, cerebro=None):
        self.x_pos = 50
        self.y_pos = self.GROUND_Y
        self.jump_stage = 0
        self.obj_width = self.WIDTH_NORMAL
        self.obj_height = self.HEIGHT_NORMAL
        self.images_normal = [pygame.image.load(img) for img in self.IMAGE_NORMALS]
        self.images_duck = [pygame.image.load(img) for img in self.IMAGE_DUCKS]
        self.image_index = 0
        self.image = self.images_normal[self.image_index]
        self.alive = True
        self.score = 0
        self.animation_timer = 0
        self.cerebro = cerebro
    def pensar(self, estado):
        """
        estado: lista o tensor con los inputs que la red necesita
        salida: 0 → no hacer nada, 1 → saltar, 2 → agacharse
        """
        if self.cerebro is None:
            return 0  # si no tiene cerebro, no hace nada

        x = torch.tensor(estado, dtype=torch.float32)
        salida = self.cerebro(x)
        # salida es un escalar entre 0 y 1 (sigmoide)
        
        # Por ejemplo, interpretamos:
        if salida.item() > 0.7:
            return 1  # saltar
        elif salida.item() < 0.3:
            return 2  # agacharse
        else:
            return 0  # seguir


    def draw(self, screen):
        screen.blit(self.image, (self.x_pos, self.y_pos))

    def esta_colisionando(self, anObject):
        return (self.x_pos + self.obj_width > anObject.x_pos and self.x_pos < anObject.x_pos + anObject.obj_width) and (self.y_pos + self.obj_height  > anObject.y_pos and self.y_pos < anObject.y_pos + anObject.obj_height)

    def update_animation(self, dt):
        """Actualiza la animación del Dino cuando corre o se agacha."""
        self.animation_timer += dt
        if self.animation_timer > 0.2:  # Cambia cada 0.2 segundos
            if self.jumping():
                # Durante el salto se muestra la imagen de salto
                self.image = pygame.image.load(self.IMAGE_JUMP)
            elif self.crouching():
                # Animación de agachado
                self.image_index = (self.image_index + 1) % len(self.images_duck)
                self.image = self.images_duck[self.image_index]
            else:
                # Animación de correr
                self.image_index = (self.image_index + 1) % len(self.images_normal)
                self.image = self.images_normal[self.image_index]

            self.animation_timer = 0


    # ---------------- MOVIMIENTO ----------------
    def update_jump(self):
        """Actualiza la posición vertical durante el salto."""
        self.y_pos = self.GROUND_Y - ((-4 * self.jump_stage * (self.jump_stage - 1)) * 172)
        self.jump_stage += 0.03
        if self.jump_stage > 1:
            self.stop_jump()

    def jump(self):
        """Inicia el salto."""
        if not self.jumping() and not self.crouching():
            self.jump_stage = 0.0001

    def stop_jump(self):
        """Termina el salto."""
        self.jump_stage = 0
        self.y_pos = self.GROUND_Y

    def crouch(self):
        """Activa el modo agachado."""
        if not self.crouching() and not self.jumping():
            self.y_pos = self.CROUCH_Y
            self.obj_width = self.WIDTH_CROUCH
            self.obj_height = self.HEIGHT_CROUCH
            # Mostrar la primera imagen de duck al iniciar
            self.image_index = 0
            self.image = self.images_duck[self.image_index]

    def stop_crouch(self):
        """Vuelve al estado normal."""
        if self.crouching():
            self.y_pos = self.GROUND_Y
            self.obj_width = self.WIDTH_NORMAL
            self.obj_height = self.HEIGHT_NORMAL
            # Volver a la animación de correr en la posición actual
            self.image_index = 0
            self.image = self.images_normal[self.image_index]

    # ---------------- ESTADO ----------------
    def jumping(self):
        return self.jump_stage > 0

    def crouching(self):
        return self.obj_width == self.WIDTH_CROUCH

    def die(self):
        self.alive = False
        self.score = 10
        quit()

    def reset(self):
        self.alive = True
        self.score = 0
        self.stop_jump()
        self.stop_crouch()

