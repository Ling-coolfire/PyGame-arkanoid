import pygame
import random

class Paddle:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.original_width = 100
        self.height = 10
        self.speed = 7
        self.color = (200, 200, 200)
        self.power_up_active = False
        self.power_up_timer = 0
        self.width = self.original_width
        self.rect = pygame.Rect(
            self.screen_width // 2 - self.width // 2,
            self.screen_height - 30,
            self.width,
            self.height
        )

    def reset(self):
        self.rect.x = self.screen_width // 2 - self.original_width // 2
        self.width = self.original_width
        self.rect.width = self.width
        self.power_up_active = False
        self.power_up_timer = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
            
        if self.power_up_active:
            self.power_up_timer -= 1
            if self.power_up_timer <= 0:
                current_center = self.rect.centerx
                self.width = self.original_width
                self.rect.width = self.width
                self.rect.centerx = current_center
                self.power_up_active = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
    def activate_power_up(self, type):
        if type == 'grow' and not self.power_up_active:
            current_center = self.rect.centerx
            self.width = 150
            self.rect.width = self.width
            self.rect.centerx = current_center
            self.power_up_active = True
            self.power_up_timer = 600 


class Ball:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.radius = 10
        self.color = (200, 200, 200)
        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.reset()

    def reset(self):
        self.rect.center = (self.screen_width // 2, self.screen_height // 2)
        self.speed_x = 6 * random.choice((1, -1))
        self.speed_y = -6

    def update(self, paddle):
        collision_object = None

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0:
            self.speed_y *= -1
            collision_object = 'wall'
        if self.rect.left <= 0 or self.rect.right >= self.screen_width:
            self.speed_x *= -1
            collision_object = 'wall'

        if self.rect.colliderect(paddle.rect) and self.speed_y > 0:
            self.speed_y *= -1
            collision_object = 'paddle'
        
        if self.rect.top > self.screen_height:
            return 'lost', None
        
        # !!! FIX !!!
        # This line ensures the function always returns a tuple,
        # fixing the "cannot unpack non-iterable NoneType object" error.
        return 'playing', collision_object

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)


class Brick:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class PowerUp:
    def __init__(self, x, y):
        self.width = 30
        self.height = 15
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.color = (60, 60, 255)
        self.speed_y = 3
        self.type = 'grow'

    def update(self):
        self.rect.y += self.speed_y

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
