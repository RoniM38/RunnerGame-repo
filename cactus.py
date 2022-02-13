import pygame

class Cactus:
    def __init__(self, surface, x, y, speed, cactus, cactuses, dino):
        self.surface = surface
        self.x = x
        self.y = y
        self.speed = speed
        self.cactus = cactus
        self.cactuses = cactuses
        self.dino = dino

        self.hitbox = self.getRect(self.cactus)

    def draw(self):
        self.surface.blit(self.cactus, (self.x, self.y))
        self.hitbox = self.getRect(self.cactus)

        # code for testing the hitboxes:
        # pygame.draw.rect(self.surface, (255, 0, 0), self.hitbox, 3)

    def move(self):
        if self.hitbox.colliderect(self.dino.hitbox):
            self.dino.collisionDetected = True

        if self.x > (self.cactus.get_width() * -1):
            self.x -= self.speed
        else:
            self.cactuses.remove(self)

    def getRect(self, img):
        width, height = img.get_size()
        width //= 2
        height //= 2
        return pygame.Rect(self.x + width // 2.1, self.y + height // 2, width//1.2, height)
