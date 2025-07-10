import pygame
import sys
import random
# !!! PHASE: POWER-UPS !!!
from game_objects import Paddle, Ball, Brick, PowerUp
# !!! END PHASE: POWER-UPS !!!

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

# !!! PHASE: POWER-UPS !!!
# --- Power-Up List ---
power_ups = []
# !!! END PHASE: POWER-UPS !!!

# --- Game Variables ---
game_state = 'playing'
score = 0
lives = 3


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
                paddle.reset()
                ball.reset()
                bricks = create_brick_wall()
                score = 0
                lives = 3
                # !!! PHASE: POWER-UPS !!!
                power_ups.clear() # Clear any lingering power-ups
                # !!! END PHASE: POWER-UPS !!!
                game_state = 'playing'

    # --- Updating Objects (only if the game is in the 'playing' state) ---
    if game_state == 'playing':
        paddle.update()
        ball_status = ball.update(paddle)

        # --- Check for Loss of a Life ---
        if ball_status == 'lost':
            lives -= 1
            if lives <= 0:
                game_state = 'game_over'
            else:
                ball.reset()
                paddle.reset()

        # --- Ball and Brick Collision ---
        for brick in bricks[:]:
            if ball.rect.colliderect(brick.rect):
                ball.speed_y *= -1
                bricks.remove(brick)
                score += 10
                # !!! PHASE: POWER-UPS !!!
                # 20% chance to drop a power-up
                if random.random() < 0.2:
                    power_up = PowerUp(brick.rect.centerx, brick.rect.centery)
                    power_ups.append(power_up)
                # !!! END PHASE: POWER-UPS !!!
                break
        
        # !!! PHASE: POWER-UPS !!!
        # --- Update and Check Power-Up Collisions ---
        for power_up in power_ups[:]:
            power_up.update()
            # Remove power-up if it goes off-screen
            if power_up.rect.top > screen_height:
                power_ups.remove(power_up)
            # Check for collision with paddle
            elif paddle.rect.colliderect(power_up.rect):
                paddle.activate_power_up(power_up.type)
                power_ups.remove(power_up)
        # !!! END PHASE: POWER-UPS !!!
        
        # --- Check for Win ---
        if not bricks:
            game_state = 'you_win'

    # --- Drawing ---
    screen.fill(BG_COLOR)
    paddle.draw(screen)
    ball.draw(screen)
    for brick in bricks:
        brick.draw(screen)
    # !!! PHASE: POWER-UPS !!!
    for power_up in power_ups:
        power_up.draw(screen)
    # !!! END PHASE: POWER-UPS !!!

    # --- Draw Score and Lives ---
    score_text = game_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    lives_text = game_font.render(f"Lives: {lives}", True, (255, 255, 255))
    screen.blit(lives_text, (screen_width - lives_text.get_width() - 10, 10))

    # --- Draw Game Over / You Win Screens ---
    if game_state == 'game_over' or game_state == 'you_win':
        if game_state == 'game_over':
            message = "GAME OVER"
        else:
            message = "YOU WIN!"
            
        text_surface = game_font.render(message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(screen_width / 2, screen_height / 2 - 20))
        screen.blit(text_surface, text_rect)
        
        restart_surface = game_font.render("Press SPACE to play again", True, (255, 255, 255))
        restart_rect = restart_surface.get_rect(center=(screen_width / 2, screen_height / 2 + 30))
        screen.blit(restart_surface, restart_rect)

    # --- Updating the Display ---
    pygame.display.flip()

    # --- Frame Rate Control ---
    clock.tick(60)
