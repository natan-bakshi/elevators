from building import *

"""
Main entry point of the project.

This script initializes the application, sets up the display window, 
and calls the necessary functions to run the simulation.
"""


pygame.init()  # Initialize pygame
pygame.mixer.init()  # Initialize mixer
pygame.mixer.music.load(DING_FILE_PATH)
clock = pygame.time.Clock()

"""    
Initializes the display window with the specified dimensions and title.
"""
window = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Elevator building')

screen_height = max(WINDOW_HEIGHT, NUM_OF_FLOORS * FLOOR_HEIGHT + 2 * MARGIN)
screen = pygame.Surface((WINDOW_WIDTH, screen_height))
background = pygame.image.load(SKY_PATH)


def blit_background():
    """
    Draws the background image onto the screen.
    """
    y = 0
    while y < screen_height:
        screen.blit(background, (0, y))
        y += background.get_height()


my_building = Building(NUM_OF_FLOORS, NUM_OF_ELEVATORS, screen)

scroll_speed = 20
scroll_y = (screen.get_height() - window.get_height())


"""
Script responsible for managing the display window and handling events during runtime.
This script initializes the display, processes user inputs, and updates the screen accordingly.
"""

running = True
while running:
    pos = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_y += scroll_y
                pos = mouse_x, mouse_y
            elif event.button == 4:  # mouse wheel up
                scroll_y -= scroll_speed
            elif event.button == 5:  # mouse wheel down
                scroll_y += scroll_speed
            scroll_y = max(0, min(screen_height - WINDOW_HEIGHT, scroll_y))

        elif event.type == pygame.MOUSEBUTTONUP:
            for floor in my_building.floors:
                floor.pushed_button = False

    blit_background()
    my_building.draw(screen)
    my_building.update(pos)
    window.blit(screen, (0, -scroll_y))

    pygame.display.flip()
