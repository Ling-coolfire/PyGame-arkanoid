import pygame
import random

class Paddle:
    def __init__(self, screen_width, screen_height):
        """
        Initializes the Paddle object.
        - screen_width, screen_height: Dimensions of the game window to handle boundaries.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Define paddle properties
        self.width = 100
        self.height = 10
        self.speed = 7
        self.color = (200, 200, 200)

        # Create the paddle's rectangle object (self.rect)
        self.rect = pygame.Rect(
            self.screen_width // 2 - self.width // 2,
            self.screen_height - 30,
            self.width,
            self.height
        )

    def update(self):
        """
        Updates the paddle's position based on keyboard input and handles boundaries.
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

    def draw(self, screen):
        """
        Draws the paddle onto the provided screen surface.
        """
        pygame.draw.rect(screen, self.color, self.rect)

# 3: Add Ball class
class Ball:
    def __init__(self, screen_width, screen_height):
        """
        Initializes the Ball object.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Define ball properties
        self.radius = 10
        self.color = (200, 200, 200)
        
        # The rect will be used for position and collision.
        # We will draw a circle at the center of this rect.
        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)

        # Call reset to set the initial position and speed
        self.reset()

    def reset(self):
        """
        Resets the ball to the center of the screen with a random initial velocity.
        """
        self.rect.center = (self.screen_width // 2, self.screen_height // 2)
        # Give the ball a random horizontal direction to start
        self.speed_x = 6 * random.choice((1, -1))
        self.speed_y = -6 # Start moving upwards

    def update(self, paddle):
        """
        Updates the ball's position and handles all collisions.
        - paddle: The player's paddle object, needed for collision checks.
        """
        # Move the ball
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off the top, left, and right walls
        if self.rect.top <= 0:
            self.speed_y *= -1
        if self.rect.left <= 0 or self.rect.right >= self.screen_width:
            self.speed_x *= -1

        # Check for collision with the paddle
        if self.rect.colliderect(paddle.rect):
            # To prevent the ball from getting "stuck" in the paddle,
            # ensure we only register the bounce when the ball is moving downwards.
            if self.speed_y > 0:
                self.speed_y *= -1
        
        # Check if the ball has fallen off the bottom of the screen (loss condition)
        if self.rect.top > self.screen_height:
            self.reset() # For now, just reset the ball

    def draw(self, screen):
        """
        Draws the ball on the screen as a circle.
        """
        pygame.draw.ellipse(screen, self.color, self.rect)

