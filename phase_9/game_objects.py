import pygame
import random

# !!! PHASE: MORE POWER-UPS !!!
# We need a font for the power-up letters.
pygame.font.init()
POWERUP_FONT = pygame.font.Font(None, 20)
# !!! END PHASE: MORE POWER-UPS !!!

class Paddle:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.original_width = 100
        self.height = 10
        self.speed = 7
        self.color = (200, 200, 200)
        
        # Power-up related attributes
        self.width = self.original_width
        
        # !!! PHASE: MORE POWER-UPS !!!
        self.power_up_timers = {
            'grow': 0,
            'laser': 0,
            'glue': 0
        }
        self.has_laser = False
        self.has_glue = False
        # !!! END PHASE: MORE POWER-UPS !!!

        self.rect = pygame.Rect(
            self.screen_width // 2 - self.width // 2,
            self.screen_height - 30,
            self.width,
            self.height
        )

    def reset(self):
        """ Resets the paddle to its starting position and clears all power-ups. """
        self.rect.x = self.screen_width // 2 - self.original_width // 2
        self.width = self.original_width
        self.rect.width = self.width
        # !!! PHASE: MORE POWER-UPS !!!
        self.has_laser = False
        self.has_glue = False
        for power_up in self.power_up_timers:
            self.power_up_timers[power_up] = 0
        # !!! END PHASE: MORE POWER-UPS !!!

    def update(self):
        """
        Updates the paddle's position, handles boundaries, and manages power-up timers.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
            
        # !!! PHASE: MORE POWER-UPS !!!
        # Handle power-up timers
        self._update_power_ups()
        # !!! END PHASE: MORE POWER-UPS !!!

    def draw(self, screen):
        """
        Draws the paddle onto the provided screen surface.
        """
        pygame.draw.rect(screen, self.color, self.rect)
        
    def activate_power_up(self, type):
        """ Activates a power-up effect on the paddle. """
        duration = 600 # 10 seconds at 60 FPS
        if type == 'grow':
            if self.power_up_timers['grow'] <= 0: # Only grow if not already grown
                current_center = self.rect.centerx
                self.width = 150
                self.rect.width = self.width
                self.rect.centerx = current_center
            self.power_up_timers['grow'] = duration
        elif type == 'laser':
            self.has_laser = True
            self.power_up_timers['laser'] = duration
        elif type == 'glue':
            self.has_glue = True
            self.power_up_timers['glue'] = duration
            
    def _update_power_ups(self):
        """ Internal method to handle countdowns and deactivation of power-ups. """
        # Grow
        if self.power_up_timers['grow'] > 0:
            self.power_up_timers['grow'] -= 1
            if self.power_up_timers['grow'] <= 0:
                current_center = self.rect.centerx
                self.width = self.original_width
                self.rect.width = self.width
                self.rect.centerx = current_center
        # Laser
        if self.power_up_timers['laser'] > 0:
            self.power_up_timers['laser'] -= 1
            if self.power_up_timers['laser'] <= 0:
                self.has_laser = False
        # Glue
        if self.power_up_timers['glue'] > 0:
            self.power_up_timers['glue'] -= 1
            if self.power_up_timers['glue'] <= 0:
                self.has_glue = False


class Ball:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.radius = 10
        self.color = (200, 200, 200)
        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        
        # !!! PHASE: MORE POWER-UPS !!!
        self.is_glued = False
        self.is_slowed = False
        self.slow_timer = 0
        self.base_speed = 6
        # !!! END PHASE: MORE POWER-UPS !!!
        
        self.reset()

    def reset(self):
        """ Resets the ball to the center and clears its states. """
        self.rect.center = (self.screen_width // 2, self.screen_height // 2)
        self.speed_x = self.base_speed * random.choice((1, -1))
        self.speed_y = -self.base_speed
        # !!! PHASE: MORE POWER-UPS !!!
        self.is_glued = False
        self.is_slowed = False
        self.slow_timer = 0
        # !!! END PHASE: MORE POWER-UPS !!!

    def update(self, paddle, launch_ball=False):
        collision_object = None

        # !!! PHASE: MORE POWER-UPS !!!
        # Handle Glued State
        if self.is_glued:
            self.rect.centerx = paddle.rect.centerx
            self.rect.bottom = paddle.rect.top
            if launch_ball:
                self.is_glued = False
                self.speed_x = self.base_speed * random.choice((1, -1))
                self.speed_y = -self.base_speed
            return 'playing', None # Don't move further if glued

        # Handle Slow State
        if self.is_slowed:
            self.slow_timer -= 1
            if self.slow_timer <= 0:
                self.speed_x = self.speed_x * 2
                self.speed_y = self.speed_y * 2
                self.is_slowed = False
        # !!! END PHASE: MORE POWER-UPS !!!

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0:
            self.speed_y *= -1
            collision_object = 'wall'
        if self.rect.left <= 0 or self.rect.right >= self.screen_width:
            self.speed_x *= -1
            collision_object = 'wall'

        if self.rect.colliderect(paddle.rect) and self.speed_y > 0:
            # !!! PHASE: MORE POWER-UPS !!!
            # Glue Power-Up Logic
            if paddle.has_glue:
                self.is_glued = True
            # !!! END PHASE: MORE POWER-UPS !!!
            self.speed_y *= -1
            collision_object = 'paddle'
        
        if self.rect.top > self.screen_height:
            return 'lost', None
        
        return 'playing', collision_object

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)
        
    # !!! PHASE: MORE POWER-UPS !!!
    def activate_power_up(self, type):
        """ Activates a power-up effect on the ball. """
        if type == 'slow' and not self.is_slowed:
            self.speed_x /= 2
            self.speed_y /= 2
            self.is_slowed = True
            self.slow_timer = 600 # 10 seconds
    # !!! END PHASE: MORE POWER-UPS !!!


class Brick:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class PowerUp:
    # !!! PHASE: MORE POWER-UPS !!!
    PROPERTIES = {
        'grow': {'color': (60, 60, 255), 'char': 'G'},
        'laser': {'color': (255, 60, 60), 'char': 'L'},
        'glue': {'color': (60, 255, 60), 'char': 'C'}, # C for Catch/Glue
        'slow': {'color': (255, 165, 0), 'char': 'S'},
    }
    # !!! END PHASE: MORE POWER-UPS !!!
    
    def __init__(self, x, y, type):
        self.width = 30
        self.height = 15
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed_y = 3
        self.type = type
        # !!! PHASE: MORE POWER-UPS !!!
        self.color = self.PROPERTIES[type]['color']
        self.char = self.PROPERTIES[type]['char']
        # !!! END PHASE: MORE POWER-UPS !!!

    def update(self):
        self.rect.y += self.speed_y

    def draw(self, screen):
        # !!! PHASE: MORE POWER-UPS !!!
        # Draw the power-up box
        pygame.draw.rect(screen, self.color, self.rect)
        # Draw the identifying letter
        text_surf = POWERUP_FONT.render(self.char, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        # !!! END PHASE: MORE POWER-UPS !!!

# !!! PHASE: MORE POWER-UPS !!!
class Laser:
    def __init__(self, x, y):
        """ Initializes the Laser object fired from the paddle. """
        self.width = 5
        self.height = 15
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.color = (255, 255, 0) # Yellow laser
        self.speed_y = -8

    def update(self):
        """ Moves the laser upwards. """
        self.rect.y += self.speed_y

    def draw(self, screen):
        """ Draws the laser. """
        pygame.draw.rect(screen, self.color, self.rect)
# !!! END PHASE: MORE POWER-UPS !!!
