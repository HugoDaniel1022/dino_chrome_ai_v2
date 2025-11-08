import pygame
import random

class Enemy:
    TYPES = {
        "cactus": {"image": "images/cactus.png", "y": 450},
        "bird": {"image": "images/bird.png", "y": 400}
    }

    def __init__(self):
        self.kind = None
        self.x_pos = 800
        self.set_random_type()

    def set_random_type(self):
        """Elige aleatoriamente si es cactus o bird y carga sus propiedades."""
        self.kind = random.choice(list(self.TYPES.keys()))
        data = self.TYPES[self.kind]
        self.image = pygame.image.load(data["image"])
        self.y_pos = data["y"]
        self.speed = 10
        self.obj_width, self.obj_height = self.image.get_size()
        self.x_pos = 800  # reaparece al borde derecho

    def update(self):
        """Mueve el enemigo y resetea si sale de la pantalla."""
        self.x_pos -= self.speed
        if self.x_pos < -self.obj_width:
            self.set_random_type()  # respawnea con tipo aleatorio

    def draw(self, screen):
        screen.blit(self.image, (self.x_pos, self.y_pos))
