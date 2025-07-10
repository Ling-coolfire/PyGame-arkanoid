import pygame
import sys
# Import both Paddle and Ball classes
from game_objects import Paddle, Ball

# -- General Setup --
pygame.init()
clock = pygame.time.Clock()

# -- Screen Setup --
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PyGame Arkanoid")

# -- Colors --
BG_COLOR = pygame.Color('grey12')

# -- Game Objects --
paddle = Paddle(screen_width, screen_height)
# !!! PHASE: Create an instance of the Ball class
ball = Ball(screen_width, screen_height)

# -- Main Game Loop --
while True:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- Updating Objects ---
    paddle.update()
    # !!! PHASE: Update the ball's position, passing the paddle for collision checks
    ball.update(paddle)

    # --- Drawing ---
    screen.fill(BG_COLOR)
    paddle.draw(screen)
    # !!! PHASE: Draw the ball
    ball.draw(screen)

    # --- Updating the Display ---
    pygame.display.flip()

    # --- Frame Rate Control ---
    clock.tick(60)
