import pygame
import random

class Paddle:
    def __init__(self, screen_width, screen_height):
        """
        Initializes the Paddle object.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.original_width = 100
        self.height = 10
        self.speed = 7
        self.color = (200, 200, 200)
        
        # !!! PHASE: POWER-UPS !!!
        # Power-up related attributes
        self.power_up_active = False
        self.power_up_timer = 0
        self.width = self.original_width
        # !!! END PHASE: POWER-UPS !!!

        self.rect = pygame.Rect(
            self.screen_width // 2 - self.width // 2,
            self.screen_height - 30,
            self.width,
            self.height
        )

    def reset(self):
        """ Resets the paddle to its starting position and size. """
        self.rect.x = self.screen_width // 2 - self.width // 2
        # !!! PHASE: POWER-UPS !!!
        self.width = self.original_width
        self.rect.width = self.width
        self.power_up_active = False
        self.power_up_timer = 0
        # !!! END PHASE: POWER-UPS !!!

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
            
        # !!! PHASE: POWER-UPS !!!
        # Handle power-up timer
        if self.power_up_active:
            self.power_up_timer -= 1
            if self.power_up_timer <= 0:
                # Power-up wears off, reset paddle size
                self.width = self.original_width
                self.rect.width = self.width
                # Center the paddle after resizing
                self.rect.x += (150 - self.original_width) // 2
                self.power_up_active = False
        # !!! END PHASE: POWER-UPS !!!

    def draw(self, screen):
        """
        Draws the paddle onto the provided screen surface.
        """
        pygame.draw.rect(screen, self.color, self.rect)
        
    # !!! PHASE: POWER-UPS !!!
    def activate_power_up(self, type):
        """ Activates a power-up effect on the paddle. """
        if type == 'grow':
            self.width = 150
            self.rect.width = self.width
            # Center the paddle after resizing
            self.rect.x -= (150 - self.original_width) // 2
            self.power_up_active = True
            # Set timer (in frames). 600 frames = 10 seconds at 60 FPS.
            self.power_up_timer = 600 
    # !!! END PHASE: POWER-UPS !!!


class Ball:
    def __init__(self, screen_width, screen_height):
        """
        Initializes the Ball object.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.radius = 10
        self.color = (200, 200, 200)
        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.reset()

    def reset(self):
        """
        Resets the ball to the center of the screen with a random initial velocity.
        """
        self.rect.center = (self.screen_width // 2, self.screen_height // 2)
        self.speed_x = 6 * random.choice((1, -1))
        self.speed_y = -6

    def update(self, paddle):
        """
        Updates the ball's position and handles collisions.
        Returns 'lost' if the ball goes off the bottom of the screen.
        """
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0:
            self.speed_y *= -1
        if self.rect.left <= 0 or self.rect.right >= self.screen_width:
            self.speed_x *= -1

        if self.rect.colliderect(paddle.rect) and self.speed_y > 0:
            self.speed_y *= -1
        
        if self.rect.top > self.screen_height:
            return 'lost'

    def draw(self, screen):
        """
        Draws the ball on the screen as a circle.
        """
        pygame.draw.ellipse(screen, self.color, self.rect)


class Brick:
    def __init__(self, x, y, width, height, color):
        """
        Initializes the Brick object.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        """
        Draws the brick onto the screen.
        """
        pygame.draw.rect(screen, self.color, self.rect)

# !!! PHASE: POWER-UPS !!!
class PowerUp:
    def __init__(self, x, y):
        """
        Initializes the PowerUp object.
        """
        self.width = 30
        self.height = 15
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.color = (60, 60, 255) # A blue color for the power-up
        self.speed_y = 3
        self.type = 'grow' # For now, only one type of power-up

    def update(self):
        """ Moves the power-up downwards. """
        self.rect.y += self.speed_y

    def draw(self, screen):
        """ Draws the power-up. """
        pygame.draw.rect(screen, self.color, self.rect)
# !!! END PHASE: POWER-UPS !!!
