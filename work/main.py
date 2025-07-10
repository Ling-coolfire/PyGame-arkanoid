import pygame
import sys

# -- General Setup --
# This is the basic setup that initializes all the modules required for PyGame.
# We also need to set up a clock to control the frame rate of our game.
pygame.init()
clock = pygame.time.Clock()

# -- Screen Setup --
# Here we define the dimensions of our game window.
# Using variables for width and height makes it easier to change them later.
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# We can set a caption for the window to give our game a title.
pygame.display.set_caption("PyGame Arkanoid")

# -- Main Game Loop --
# The game loop is the heart of any PyGame program. It's a `while` loop that
# runs continuously, handling events, updating game state, and drawing to the screen.
while True:
    # --- Event Handling ---
    # This `for` loop checks for any events that have happened since the last frame.
    # Events can be key presses, mouse movements, or, in this case, closing the window.
    for event in pygame.event.get():
        # The `pygame.QUIT` event is triggered when the user clicks the 'X' button
        # on the window.
        if event.type == pygame.QUIT:
            # If the QUIT event is detected, we first shut down PyGame cleanly.
            pygame.quit()
            # Then, we exit the program using `sys.exit()`.
            sys.exit()

    # --- Drawing ---
    # This is where all the rendering will happen in later steps.
    # For now, we'll just fill the screen with a solid color.
    # Colors are represented by RGB tuples (Red, Green, Blue).
    # (0, 0, 0) is black.
    screen.fill((0, 0, 0))

    # --- Updating the Display ---
    # `pygame.display.flip()` updates the entire screen with everything we've drawn
    # in the current frame. This is what makes our drawings visible.
    pygame.display.flip()

    # --- Frame Rate Control ---
    # `clock.tick(60)` tells PyGame to pause for the right amount of time to ensure
    # our game runs at a maximum of 60 frames per second (FPS). This keeps the
    # game's speed consistent across different computers.
    clock.tick(60)

