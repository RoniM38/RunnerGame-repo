import pygame

class Dino:
    def __init__(self, surface, x, y, idle_dino, dead_dino, walk_animation, bend_animation,
                 logoX, player):
        self.surface = surface
        self.x = x
        self.y = y
        self.idle = idle_dino
        self.dead_dino = dead_dino
        self.walk_animation = walk_animation
        self.bend_animation = bend_animation
        self.logoX = logoX
        self.player = player

        self.count = 0

        self.isJumping = False
        self.jumpCount = 0

        self.isBending = False

        self.hitbox = self.getRect(self.idle)
        self.collisionDetected = False
        game_over_font = pygame.font.SysFont("Berlin Sans FB Demi", 80, "bold")
        self.game_over_label = game_over_font.render("GAME OVER", True, (56, 56, 56))

    def draw(self):
        if not self.collisionDetected:
            self.player.score += 0.15
            if self.isJumping:
                self.surface.blit(self.idle, (self.x, self.y))
                self.hitbox = self.getRect(self.idle)
            elif self.isBending:
                frame = self.bend_animation[self.count]
                self.surface.blit(frame, (self.x, self.y))
                self.hitbox = self.getRect(frame)
            else:
                frame = self.walk_animation[self.count]
                self.surface.blit(frame, (self.x, self.y))
                self.hitbox = self.getRect(frame)
        else:
            self.surface.blit(self.dead_dino, (self.x, self.y))
            self.hitbox = self.getRect(self.dead_dino)
            self.surface.blit(self.game_over_label, (self.logoX-50, 100))

        # code for testing the hitboxes:
        # pygame.draw.rect(self.surface, (255, 0, 0), self.hitbox, 3)

    def run(self):
        self.count = (self.count + 1) % len(self.walk_animation)
        self.draw()

    def jump(self, jumpMax):
        self.y -= self.jumpCount
        if self.jumpCount > -jumpMax:
            self.jumpCount -= 1
        else:
            self.isJumping = False

    def getRect(self, img):
        width, height = img.get_size()
        width //= 2
        height //= 2

        if img in self.bend_animation:
            bendX = self.x + width // 2 - 15
            bendY = self.y + height // 2 + 35
            return pygame.Rect(bendX, bendY, width + 25, height - 52)
        else:
            return pygame.Rect(self.x + width // 2, self.y + height // 2, width, height)
