import pygame
import sys
import random
from game_objects import Paddle, Ball, Brick, PowerUp

# -- General Setup --
pygame.init()
# !!! PHASE: SOUND EFFECTS !!!
# Initialize the mixer module for sound
pygame.mixer.init()
# !!! END PHASE: SOUND EFFECTS !!!
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

# !!! PHASE: SOUND EFFECTS !!!
# -- Sound Setup --
# Load your sound files here. Make sure they are in the same directory as your script.
try:
    bounce_sound = pygame.mixer.Sound('bounce.wav')
    brick_break_sound = pygame.mixer.Sound('brick_break.wav')
    game_over_sound = pygame.mixer.Sound('game_over.wav')
except pygame.error as e:
    print(f"Warning: Sound file not found. {e}")
    # Create dummy sound objects if files are not found, so the game doesn't crash
    class DummySound:
        def play(self): pass
    bounce_sound = DummySound()
    brick_break_sound = DummySound()
    game_over_sound = DummySound()
# !!! END PHASE: SOUND EFFECTS !!!

# -- Game Objects --
paddle = Paddle(screen_width, screen_height)
ball = Ball(screen_width, screen_height)

# --- Brick Wall Setup Function ---
def create_brick_wall():
    # ... (rest of the function is unchanged)
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
power_ups = []

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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if game_state != 'playing':
                paddle.reset()
                ball.reset()
                bricks = create_brick_wall()
                score = 0
                lives = 3
                power_ups.clear()
                game_state = 'playing'

    # --- Updating Objects ---
    if game_state == 'playing':
        paddle.update()
        # !!! PHASE: SOUND EFFECTS !!!
        # The ball's update method now also returns information about what it hit
        ball_status, collision_object = ball.update(paddle)
        # !!! END PHASE: SOUND EFFECTS !!!

        if ball_status == 'lost':
            lives -= 1
            if lives <= 0:
                game_state = 'game_over'
                # !!! PHASE: SOUND EFFECTS !!!
                game_over_sound.play()
                # !!! END PHASE: SOUND EFFECTS !!!
            else:
                ball.reset()
                paddle.reset()
        # !!! PHASE: SOUND EFFECTS !!!
        elif collision_object in ['wall', 'paddle']:
            bounce_sound.play()
        # !!! END PHASE: SOUND EFFECTS !!!

        for brick in bricks[:]:
            if ball.rect.colliderect(brick.rect):
                ball.speed_y *= -1
                bricks.remove(brick)
                score += 10
                # !!! PHASE: SOUND EFFECTS !!!
                brick_break_sound.play()
                # !!! END PHASE: SOUND EFFECTS !!!
                if random.random() < 0.2:
                    power_up = PowerUp(brick.rect.centerx, brick.rect.centery)
                    power_ups.append(power_up)
                break
        
        for power_up in power_ups[:]:
            power_up.update()
            if power_up.rect.top > screen_height:
                power_ups.remove(power_up)
            elif paddle.rect.colliderect(power_up.rect):
                paddle.activate_power_up(power_up.type)
                power_ups.remove(power_up)
        
        if not bricks:
            game_state = 'you_win'

    # --- Drawing ---
    screen.fill(BG_COLOR)
    paddle.draw(screen)
    ball.draw(screen)
    for brick in bricks:
        brick.draw(screen)
    for power_up in power_ups:
        power_up.draw(screen)

    score_text = game_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    lives_text = game_font.render(f"Lives: {lives}", True, (255, 255, 255))
    screen.blit(lives_text, (screen_width - lives_text.get_width() - 10, 10))

    if game_state != 'playing':
        message = "GAME OVER" if game_state == 'game_over' else "YOU WIN!"
        text_surface = game_font.render(message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(screen_width / 2, screen_height / 2 - 20))
        screen.blit(text_surface, text_rect)
        
        restart_surface = game_font.render("Press SPACE to play again", True, (255, 255, 255))
        restart_rect = restart_surface.get_rect(center=(screen_width / 2, screen_height / 2 + 30))
        screen.blit(restart_surface, restart_rect)

    pygame.display.flip()
    clock.tick(60)
