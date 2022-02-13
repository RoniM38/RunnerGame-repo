import pygame
import random
import sys
import os

from background import BackGround
from player import Player
from dino import Dino
from cactus import Cactus

pygame.init()

WINDOW_SIZE = (1100, 550)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Dino Run")

WHITE = (255, 255, 255)
DARK_GREY = (56, 56, 56)
LIGHT_GREY = (105, 105, 105)

DINO_X = WINDOW_SIZE[0] // 2.5
DINO_Y = WINDOW_SIZE[1] - 210
logoX = WINDOW_SIZE[0] // 3

# Dino images
idle_dino = pygame.image.load("Dino/dino.png")
idle_dino = pygame.transform.scale(idle_dino, (200, 200))
dead_dino = pygame.image.load("Dino/deadDino.png")
dead_dino = pygame.transform.scale(dead_dino, (200, 200))
# loading the animation frames into a list
dino_walk_animation = [pygame.image.load("Dino/DinoWalk/" + img) for img in os.listdir("Dino/DinoWalk")]
dino_bend_animation = [pygame.image.load("Dino/DinoBend/" + img) for img in os.listdir("Dino/DinoBend")]
# scaling the animation frames in the list
dino_walk_animation = [pygame.transform.scale(i, (200, 200)) for i in dino_walk_animation]
dino_bend_animation = [pygame.transform.scale(i, (200, 200)) for i in dino_bend_animation]

# Cactuses images
cactus_sprites = [pygame.image.load("Cactuses/" + img) for img in os.listdir("Cactuses")]

# Background image
BG = pygame.image.load("DesignAssets/BG.png")
BG = pygame.transform.scale(BG, (WINDOW_SIZE[0], BG.get_height()))

# Replay Button Image
replay_img = pygame.image.load("DesignAssets/replayButton.png")


def main():
    player = Player(window, DARK_GREY)

    JUMP_MAX = 18
    dino = Dino(window, DINO_X, DINO_Y, idle_dino, dead_dino, dino_walk_animation,
                dino_bend_animation, logoX, player)
    time = 0

    scrollSpeed = 8
    y = WINDOW_SIZE[1] - BG.get_height() - 30
    background = BackGround(window, 0, y, scrollSpeed, BG)

    # waitTime / 60 (fps) = actual wait time
    waitTime = 10

    # time waited between each cactus spawn in ms
    cactusWait = 2000
    # starting wait - 0
    wait = 0
    start = pygame.time.get_ticks()
    cactuses = []

    clock = pygame.time.Clock()
    fps_font = pygame.font.SysFont("Arial", 30, "bold")

    replayButton = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if (not dino.isJumping and not dino.isBending) and \
                        (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                    dino.isJumping = True
                    dino.jumpCount = JUMP_MAX

                if event.key == pygame.K_q:
                    menu()

            if event.type == pygame.MOUSEBUTTONDOWN and replayButton is not None:
                if replayButton.collidepoint(event.pos):
                    menu()

            if (event.type == pygame.KEYDOWN and
                (event.key == pygame.K_SPACE or event.key == pygame.K_UP)) and \
                    replayButton is not None:
                menu()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            dino.isBending = True
        else:
            dino.isBending = False

        time += 1
        window.fill(WHITE)
        if not dino.collisionDetected:
            background.scroll()
        background.draw()

        clock.tick(60)
        window.blit(fps_font.render(f"FPS:{int(clock.get_fps())}", True, DARK_GREY),
                    (10, WINDOW_SIZE[1]-50))

        if not dino.collisionDetected:
            if dino.isJumping:
                dino.jump(JUMP_MAX)
            else:
                if time % waitTime == 0:
                    dino.run()
        dino.draw()

        now = pygame.time.get_ticks()
        if player.score >= 30 and now - start >= wait:
            wait = cactusWait
            start = pygame.time.get_ticks()

            chosenCactus = random.choice(cactus_sprites)
            size = random.randint(100, 150)
            chosenCactus = pygame.transform.scale(chosenCactus, (size, size))

            cactus = Cactus(window, WINDOW_SIZE[0]+200, background.y-size+size//2,
                            scrollSpeed, chosenCactus, cactuses, dino)
            cactuses.append(cactus)

        for cactus in cactuses:
            if not dino.collisionDetected:
                cactus.move()
            cactus.draw()

        if dino.collisionDetected:
            replayButton = window.blit(replay_img, (logoX+50, 120))

        if player.score > 0 and player.score % 50 == 0:
            scrollSpeed += 2
            cactusWait -= 150

        player.displayScore()

        pygame.display.update()

    pygame.quit()
    sys.exit(0)


def menu():
    font = pygame.font.SysFont("Arial", 30, "bold")
    font2 = pygame.font.SysFont("Berlin Sans FB Demi", 80, "bold")
    logo = font2.render("DINO RUN", True, DARK_GREY)
    playLabel = font.render("Press Space to Play", True, LIGHT_GREY)
    devLabel = font.render("By Roni", True, DARK_GREY)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    main()

        window.fill(WHITE)
        y = WINDOW_SIZE[1] - BG.get_height() - 30
        window.blit(BG, (0, y))
        window.blit(idle_dino, (DINO_X, DINO_Y))
        window.blit(playLabel, (10, WINDOW_SIZE[1] - 60))
        window.blit(logo, (logoX, 100))
        window.blit(devLabel, (logoX+140, 190))

        pygame.display.update()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    menu()
