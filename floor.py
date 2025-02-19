from config import *
import pygame


def draw_space(screen, top_left, space_color):
    """
    Draws a spacer between floors.
    Args:
        screen (pygame.Surface): The surface to draw on.
        top_left (tuple): (x, y) coordinates of the top-left corner.
        space_color (tuple): RGB color of the spacer.
    """
    x, y = top_left
    pygame.draw.rect(screen, space_color, pygame.Rect(x, y, FLOOR_WIDTH, FLOOR_SPACER_HEIGHT))


class Floor:
    """ Represents a floor in the building. """
    def __init__(self, level):
        self.level = level  # Floor number
        self.button_center = None  # Call button center position
        self.pushed_button = False  # Call button state
        self.top_left = None  # Top-left position of the floor
        self.button_color = RED  # Call button color
        self.timer = None  # Initial timer value
        self.start_time = 0  # Time when the call button was pressed


    def button_pressed(self, x, y):
        """
        Checks if the call button was pressed.
        Args:
            x (int): X-coordinate of the click.
            y (int): Y-coordinate of the click.
        Returns:
            int or None: Floor level if pressed, otherwise None.
        """
        cx, cy = self.button_center
        if ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 <= BUTTON_RADIUS:
            return self.level


    def draw_number(self, screen, center):
        """
        Draws the floor number on the screen.
        Args:
            screen (pygame.Surface): The surface to draw on.
            center (tuple): The (x, y) position for the number.
        """
        font = pygame.font.Font(None, 25)
        font.set_bold(True)
        number = font.render(str(self.level + 1), True, self.button_color)
        number_pos = number.get_rect(center=center)
        screen.blit(number, number_pos)


    def draw_button(self, screen, center):
        """
        Draws the floor call button, including its shadow and number.
        Args:
            screen (pygame.Surface): The surface to draw on.
            center (tuple): The (x, y) position of the button.
        """
        if self.pushed_button:
            shadow_surface = pygame.Surface((BUTTON_RADIUS * 2, BUTTON_RADIUS * 2), pygame.SRCALPHA)
            shadow_center = BUTTON_RADIUS, BUTTON_RADIUS
            pygame.draw.circle(shadow_surface, BUTTON_SHADOW_COLOR, shadow_center, BUTTON_RADIUS + 2)
            x, y = center
            shadow_top_left = x - BUTTON_RADIUS, y - BUTTON_RADIUS
            screen.blit(shadow_surface, shadow_top_left)
        pygame.draw.circle(screen, CENTER_BUTTON_COLOR, center, BUTTON_RADIUS)
        pygame.draw.circle(screen, self.button_color, center, BUTTON_RADIUS, width=3)
        self.button_center = center
        self.draw_number(screen, center)


    def draw_timer(self, screen, center):
        """
        Draws and updates the floor button timer on the screen.
        Args:
            screen (pygame.Surface): The surface to draw on.
            center (tuple): The (x, y) position of the timer.
        """
        if self.timer:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.start_time
            self.timer -= elapsed_time
            remaining_time = max(0.0, self.timer) / 1000  # Change from ms to second
            timer_text = f"{remaining_time:.1f}"
            front_font = pygame.font.Font(None, TEXT_NUMBER_FLOOR_SIZE)
            back_font = pygame.font.Font(None, TEXT_NUMBER_FLOOR_SIZE)  # Creates a frame to highlight text
            back_font.set_bold(True)
            timer_back_render = back_font.render(timer_text, True, OUTLINE_TIMER_COLOR)
            timer_front_render = front_font.render(timer_text, True, BLACK)
            timer_pos = timer_back_render.get_rect(center=center)
            screen.blit(timer_back_render, timer_pos)
            timer_pos = timer_front_render.get_rect(center=center)
            screen.blit(timer_front_render, timer_pos)
            self.start_time = current_time


    def draw(self, screen, image, space_color=BLACK, button_down=None):
        """
        Draws the floor, including its background, button, and timer.
        Args:
            screen (pygame.Surface): The surface to draw on.
            image (pygame.Surface): The floor background image.
            space_color (tuple, optional): The color of the space area. Defaults to BLACK.
            button_down (bool, optional): Indicates if the button is pressed. Defaults to None.
        """
        base_height = screen.get_height() - FLOOR_HEIGHT - MARGIN
        self.top_left = top_left = (MARGIN, base_height - self.level * FLOOR_HEIGHT)
        screen.blit(image, top_left)
        draw_space(screen, top_left, space_color)
        x, y = top_left
        button_center = (x + FLOOR_WIDTH // 2 + CENTER_BUTTON_SPASE, y + (FLOOR_HEIGHT + FLOOR_SPACER_HEIGHT) // 2)
        timer_center = (x + FLOOR_WIDTH // 2 - CENTER_TIMER_SPASE, y + (FLOOR_HEIGHT + FLOOR_SPACER_HEIGHT) // 2)
        self.draw_button(screen, button_center)
        self.draw_timer(screen, timer_center)

