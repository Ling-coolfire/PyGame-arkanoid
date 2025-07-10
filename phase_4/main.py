import pygame
import sys
# !!! PHASE: ADD BRICKS !!!
# Import Paddle, Ball, and the new Brick class
from game_objects import Paddle, Ball, Brick
# !!! END PHASE: ADD BRICKS !!!

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
# !!! PHASE: ADD BRICKS !!!
BRICK_COLORS = [(178, 34, 34), (255, 165, 0), (255, 215, 0), (50, 205, 50)] # Red, Orange, Yellow, Green
# !!! END PHASE: ADD BRICKS !!!

# -- Game Objects --
paddle = Paddle(screen_width, screen_height)
ball = Ball(screen_width, screen_height)

# !!! PHASE: ADD BRICKS !!!
# --- Brick Wall Setup ---
bricks = []
brick_rows = 4
brick_cols = 10
brick_width = 75
brick_height = 20
brick_padding = 5
wall_start_y = 50

for row in range(brick_rows):
    for col in range(brick_cols):
        # Calculate the x and y position for each brick
        x = col * (brick_width + brick_padding) + brick_padding
        y = row * (brick_height + brick_padding) + wall_start_y
        # Get a color for the current row
        color = BRICK_COLORS[row % len(BRICK_COLORS)]
        # Create a Brick object and add it to our list
        bricks.append(Brick(x, y, brick_width, brick_height, color))
# !!! END PHASE: ADD BRICKS !!!


# -- Main Game Loop --
while True:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- Updating Objects ---
    paddle.update()
    ball.update(paddle)

    # !!! PHASE: ADD BRICKS !!!
    # --- Ball and Brick Collision ---
    # We iterate over a copy of the list (bricks[:]) because we might modify
    # the original list inside the loop, which can cause errors.
    for brick in bricks[:]:
        if ball.rect.colliderect(brick.rect):
            # Reverse the ball's vertical direction
            ball.speed_y *= -1
            # Remove the brick from the list
            bricks.remove(brick)
            # Break the loop to prevent the ball from hitting multiple bricks in one frame
            break
    # !!! END PHASE: ADD BRICKS !!!

    # --- Drawing ---
    screen.fill(BG_COLOR)
    paddle.draw(screen)
    ball.draw(screen)
    
    # !!! PHASE: ADD BRICKS !!!
    # --- Draw all the bricks ---
    for brick in bricks:
        brick.draw(screen)
    # !!! END PHASE: ADD BRICKS !!!

    # --- Updating the Display ---
    pygame.display.flip()

    # --- Frame Rate Control ---
    clock.tick(60)
