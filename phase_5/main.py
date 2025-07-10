import pygame
import sys
from game_objects import Paddle, Ball, Brick

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
BRICK_COLORS = [(178, 34, 34), (255, 165, 0), (255, 215, 0), (50, 205, 50)]

# !!! PHASE: WIN/LOSS STATE !!!
# -- Font Setup --
# We need a font to display messages on the screen.
game_font = pygame.font.Font(None, 40)
# !!! END PHASE: WIN/LOSS STATE !!!

# -- Game Objects --
paddle = Paddle(screen_width, screen_height)
ball = Ball(screen_width, screen_height)

# !!! PHASE: WIN/LOSS STATE !!!
# --- Brick Wall Setup Function ---
# We put the brick creation logic into a function to easily rebuild the wall.
def create_brick_wall():
    bricks = []
    brick_rows = 4
    brick_cols = 10
    brick_width = 75
    brick_height = 20
    brick_padding = 5
    wall_start_y = 50
    for row in range(brick_rows):
        for col in range(brick_cols):
            x = col * (brick_width + brick_padding) + brick_padding
            y = row * (brick_height + brick_padding) + wall_start_y
            color = BRICK_COLORS[row % len(BRICK_COLORS)]
            bricks.append(Brick(x, y, brick_width, brick_height, color))
    return bricks

# Create the initial wall of bricks
bricks = create_brick_wall()

# --- Game State Variable ---
game_state = 'playing' # Can be 'playing', 'game_over', or 'you_win'
# !!! END PHASE: WIN/LOSS STATE !!!


# -- Main Game Loop --
while True:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # !!! PHASE: WIN/LOSS STATE !!!
        # --- Restart Logic ---
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if game_state != 'playing':
                # Reset the game objects to their starting state
                paddle.reset()
                ball.reset()
                bricks = create_brick_wall()
                game_state = 'playing'
        # !!! END PHASE: WIN/LOSS STATE !!!

    # --- Updating Objects (only if the game is in the 'playing' state) ---
    if game_state == 'playing':
        paddle.update()
        ball_status = ball.update(paddle)

        # !!! PHASE: WIN/LOSS STATE !!!
        # --- Check for Loss ---
        if ball_status == 'lost':
            game_state = 'game_over'

        # --- Ball and Brick Collision ---
        for brick in bricks[:]:
            if ball.rect.colliderect(brick.rect):
                ball.speed_y *= -1
                bricks.remove(brick)
                break
        
        # --- Check for Win ---
        if not bricks:
            game_state = 'you_win'
        # !!! END PHASE: WIN/LOSS STATE !!!

    # --- Drawing ---
    screen.fill(BG_COLOR)
    paddle.draw(screen)
    ball.draw(screen)
    for brick in bricks:
        brick.draw(screen)

    # !!! PHASE: WIN/LOSS STATE !!!
    # --- Draw Game Over / You Win Screens ---
    if game_state == 'game_over':
        text_surface = game_font.render("GAME OVER", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(screen_width / 2, screen_height / 2 - 20))
        screen.blit(text_surface, text_rect)
        
        restart_surface = game_font.render("Press SPACE to play again", True, (255, 255, 255))
        restart_rect = restart_surface.get_rect(center=(screen_width / 2, screen_height / 2 + 30))
        screen.blit(restart_surface, restart_rect)

    elif game_state == 'you_win':
        text_surface = game_font.render("YOU WIN!", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(screen_width / 2, screen_height / 2 - 20))
        screen.blit(text_surface, text_rect)

        restart_surface = game_font.render("Press SPACE to play again", True, (255, 255, 255))
        restart_rect = restart_surface.get_rect(center=(screen_width / 2, screen_height / 2 + 30))
        screen.blit(restart_surface, restart_rect)
    # !!! END PHASE: WIN/LOSS STATE !!!

    # --- Updating the Display ---
    pygame.display.flip()

    # --- Frame Rate Control ---
    clock.tick(60)
