import pygame

class Player:
    def __init__(self, surface, DARK_GREY):
        self.surface = surface
        self.DARK_GREY = DARK_GREY

        self.score_font = pygame.font.SysFont("Arial", 30, "bold")
        self.score = 0

        with open("highscore.txt", "r") as f:
            self.highscore = int(f.read())

    def displayScore(self):
        if self.score > self.highscore:
            self.highscore = int(self.score)

            with open("highscore.txt", "w") as f:
                f.write(str(self.highscore))

        self.surface.blit(self.score_font.render(f"SCORE:{int(self.score)}", True, self.DARK_GREY), (10, 10))
        self.surface.blit(self.score_font.render(f"BEST:{self.highscore}", True, self.DARK_GREY), (10, 50))
