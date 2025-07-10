import pygame
import sys
import random
# !!! PHASE: MORE POWER-UPS !!!
from game_objects import Paddle, Ball, Brick, PowerUp, Laser
# !!! END PHASE: MORE POWER-UPS !!!

# -- General Setup --
pygame.init()
pygame.mixer.init()
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

# -- Sound Setup --
try:
    bounce_sound = pygame.mixer.Sound('bounce.wav')
    brick_break_sound = pygame.mixer.Sound('brick_break.wav')
    game_over_sound = pygame.mixer.Sound('game_over.wav')
    # !!! PHASE: MORE POWER-UPS !!!
    laser_sound = pygame.mixer.Sound('laser.wav')
    # !!! END PHASE: MORE POWER-UPS !!!
except pygame.error as e:
    print(f"Warning: Sound file not found. {e}")
    class DummySound:
        def play(self): pass
    bounce_sound, brick_break_sound, game_over_sound, laser_sound = DummySound(), DummySound(), DummySound(), DummySound()

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
power_ups = []
# !!! PHASE: MORE POWER-UPS !!!
lasers = []
# !!! END PHASE: MORE POWER-UPS !!!

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
        if event.type == pygame.KEYDOWN:
            # --- Restart Logic ---
            if event.key == pygame.K_SPACE and game_state != 'playing':
                paddle.reset()
                ball.reset()
                bricks = create_brick_wall()
                score = 0
                lives = 3
                power_ups.clear()
                lasers.clear()
                game_state = 'playing'
            
            # !!! PHASE: MORE POWER-UPS !!!
            # --- Launch Glued Ball ---
            if event.key == pygame.K_SPACE and ball.is_glued:
                ball.is_glued = False # The update method will handle the launch
            
            # --- Fire Laser ---
            if event.key == pygame.K_f and paddle.has_laser:
                # Fire two lasers, one from each side of the paddle
                lasers.append(Laser(paddle.rect.centerx - 30, paddle.rect.top))
                lasers.append(Laser(paddle.rect.centerx + 30, paddle.rect.top))
                laser_sound.play()
            # !!! END PHASE: MORE POWER-UPS !!!

    # --- Updating Objects ---
    if game_state == 'playing':
        paddle.update()
        # !!! PHASE: MORE POWER-UPS !!!
        # Pass spacebar press state to ball update for launching
        keys = pygame.key.get_pressed()
        ball_status, collision_object = ball.update(paddle, keys[pygame.K_SPACE])
        # !!! END PHASE: MORE POWER-UPS !!!

        if ball_status == 'lost':
            lives -= 1
            if lives <= 0:
                game_state = 'game_over'
                game_over_sound.play()
            else:
                ball.reset()
                paddle.reset()
        elif collision_object in ['wall', 'paddle']:
            bounce_sound.play()

        # --- Ball and Brick Collision ---
        for brick in bricks[:]:
            if ball.rect.colliderect(brick.rect):
                ball.speed_y *= -1
                bricks.remove(brick)
                score += 10
                brick_break_sound.play()
                # !!! PHASE: MORE POWER-UPS !!!
                # 30% chance to drop a power-up
                if random.random() < 0.3:
                    power_up_type = random.choice(['grow', 'laser', 'glue', 'slow'])
                    power_up = PowerUp(brick.rect.centerx, brick.rect.centery, power_up_type)
                    power_ups.append(power_up)
                # !!! END PHASE: MORE POWER-UPS !!!
                break
        
        # --- Power-Up Logic ---
        for power_up in power_ups[:]:
            power_up.update()
            if power_up.rect.top > screen_height:
                power_ups.remove(power_up)
            elif paddle.rect.colliderect(power_up.rect):
                if power_up.type in ['grow', 'laser', 'glue']:
                    paddle.activate_power_up(power_up.type)
                elif power_up.type == 'slow':
                    ball.activate_power_up(power_up.type)
                power_ups.remove(power_up)
        
        # !!! PHASE: MORE POWER-UPS !!!
        # --- Laser Logic ---
        for laser in lasers[:]:
            laser.update()
            if laser.rect.bottom < 0:
                lasers.remove(laser)
            else:
                # Check for laser collision with bricks
                for brick in bricks[:]:
                    if laser.rect.colliderect(brick.rect):
                        bricks.remove(brick)
                        lasers.remove(laser)
                        score += 10
                        brick_break_sound.play()
                        break # A laser can only destroy one brick
        # !!! END PHASE: MORE POWER-UPS !!!
        
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
    # !!! PHASE: MORE POWER-UPS !!!
    for laser in lasers:
        laser.draw(screen)
    # !!! END PHASE: MORE POWER-UPS !!!

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
