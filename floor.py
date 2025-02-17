from config import *
import pygame


def draw_space(screen, top_left, space_color):
    x, y = top_left
    pygame.draw.rect(screen, space_color, pygame.Rect(x, y, FLOOR_WIDTH, FLOOR_SPACER_HEIGHT))


class Floor:
    def __init__(self, level):
        self.level = level
        self.index = None
        self.button_center = None
        self.pushed_button = False
        self.top_left = None
        self.button_color = RED
        self.timer = 0.0
        self.start_time = 0

    def button_pressed(self, x, y):
        cx, cy = self.button_center
        if ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 <= BUTTON_RADIUS:
            return self.level

    def draw_number(self, screen, center):
        font = pygame.font.Font(None, 25)
        font.set_bold(True)
        number = font.render(str(self.level + 1), True, self.button_color)
        number_pos = number.get_rect(center=center)
        screen.blit(number, number_pos)

    def draw_button(self, screen, center):
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
        base_height = screen.get_height() - FLOOR_HEIGHT - MARGIN
        self.top_left = top_left = (MARGIN, base_height - self.level * FLOOR_HEIGHT)
        screen.blit(image, top_left)
        draw_space(screen, top_left, space_color)
        x, y = top_left
        button_center = (x + FLOOR_WIDTH // 2 + CENTER_BUTTON_SPASE, y + (FLOOR_HEIGHT + FLOOR_SPACER_HEIGHT) // 2)
        timer_center = (x + FLOOR_WIDTH // 2 - CENTER_TIMER_SPASE, y + (FLOOR_HEIGHT + FLOOR_SPACER_HEIGHT) // 2)
        self.draw_button(screen, button_center)
        self.draw_timer(screen, timer_center)

