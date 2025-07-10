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

# -- Font Setup --
game_font = pygame.font.Font(None, 40)

# -- Game Objects --
paddle = Paddle(screen_width, screen_height)
ball = Ball(screen_width, screen_height)

# --- Brick Wall Setup Function ---
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

bricks = create_brick_wall()

# !!! PHASE: SCORE & LIVES !!!
# --- Game Variables ---
game_state = 'playing'
score = 0
lives = 3
# !!! END PHASE: SCORE & LIVES !!!


# -- Main Game Loop --
while True:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # --- Restart Logic ---
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if game_state != 'playing':
                # Reset the game objects to their starting state
                paddle.reset()
                ball.reset()
                bricks = create_brick_wall()
                # !!! PHASE: SCORE & LIVES !!!
                score = 0
                lives = 3
                # !!! END PHASE: SCORE & LIVES !!!
                game_state = 'playing'

    # --- Updating Objects (only if the game is in the 'playing' state) ---
    if game_state == 'playing':
        paddle.update()
        ball_status = ball.update(paddle)

        # !!! PHASE: SCORE & LIVES !!!
        # --- Check for Loss of a Life ---
        if ball_status == 'lost':
            lives -= 1
            if lives <= 0:
                game_state = 'game_over'
            else:
                # Reset ball and paddle position for the next life
                ball.reset()
                paddle.reset()
        # !!! END PHASE: SCORE & LIVES !!!

        # --- Ball and Brick Collision ---
        for brick in bricks[:]:
            if ball.rect.colliderect(brick.rect):
                ball.speed_y *= -1
                bricks.remove(brick)
                # !!! PHASE: SCORE & LIVES !!!
                score += 10 # Increase score when a brick is hit
                # !!! END PHASE: SCORE & LIVES !!!
                break
        
        # --- Check for Win ---
        if not bricks:
            game_state = 'you_win'

    # --- Drawing ---
    screen.fill(BG_COLOR)
    paddle.draw(screen)
    ball.draw(screen)
    for brick in bricks:
        brick.draw(screen)

    # !!! PHASE: SCORE & LIVES !!!
    # --- Draw Score and Lives ---
    score_text = game_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    lives_text = game_font.render(f"Lives: {lives}", True, (255, 255, 255))
    screen.blit(lives_text, (screen_width - lives_text.get_width() - 10, 10))
    # !!! END PHASE: SCORE & LIVES !!!

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

    # --- Updating the Display ---
    pygame.display.flip()

    # --- Frame Rate Control ---
    clock.tick(60)
