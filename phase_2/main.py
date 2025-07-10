import pygame
import sys
# NEW: We import the Paddle class from our new file.
from game_objects import Paddle

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
# Now, instead of a simple Rect, we create an *instance* of our Paddle class.
paddle = Paddle(screen_width, screen_height)

# -- Main Game Loop --
while True:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- Updating Objects ---
    # The main loop no longer needs to know the details of how the paddle works.
    # It just tells the paddle to update itself.
    paddle.update()

    # --- Drawing ---
    screen.fill(BG_COLOR)
    # We tell the paddle to draw itself to the screen.
    paddle.draw(screen)

    # --- Updating the Display ---
    pygame.display.flip()

    # --- Frame Rate Control ---
    clock.tick(60)
