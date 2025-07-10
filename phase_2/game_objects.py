import pygame

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
        # It's placed at the bottom-center of the screen.
        self.rect = pygame.Rect(
            self.screen_width // 2 - self.width // 2,
            self.screen_height - 30,
            self.width,
            self.height
        )

    def update(self):
        """
        Updates the paddle's position based on keyboard input and handles boundaries.
        This method is called once every frame from the main loop.
        """
        # Get all the keys currently being pressed
        keys = pygame.key.get_pressed()

        # Move left if the left arrow key is pressed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        # Move right if the right arrow key is pressed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Boundary checking to keep the paddle on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width

    def draw(self, screen):
        """
        Draws the paddle onto the provided screen surface.
        - screen: The main pygame screen object to draw on.
        """
        pygame.draw.rect(screen, self.color, self.rect)
