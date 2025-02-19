from elevator import *
from floor import *


class Building:
    """Manages floors, elevators, and their interactions."""
    def __init__(self, num_of_floors, num_of_elevators, screen):
        self.floors = [Floor(i) for i in range(num_of_floors)]  # List of floors
        self.elevators = [Elevator(i, self) for i in range(num_of_elevators)]  # List of elevators
        for elevator in self.elevators:
            elevator.y = elevator.final = screen.get_height() - MARGIN - FLOOR_HEIGHT + FLOOR_SPACER_HEIGHT  # Initial position


    def draw(self, screen, button_down=None):
        """
        Draws the building, including floors and elevators.
        Args:
            screen: The Pygame surface to draw on.
            button_down (optional): Indicates if a button is currently pressed.
        Loads and scales the floor and elevator images, then draws each floor
        and elevator on the screen.
        """
        elevator_img = pygame.image.load(ELEVATOR_IMAGE_PATH).convert_alpha()
        scaled_elevator_img = pygame.transform.scale(elevator_img, ELEVATOR_SIZE)
        floor_img = pygame.image.load(FLOOR_IMAGE_PATH)
        scaled_floor_image = pygame.transform.scale(floor_img, (FLOOR_WIDTH, FLOOR_HEIGHT))

        for floor in self.floors[:-1]:
            floor.draw(screen, scaled_floor_image, button_down=button_down)
        self.floors[-1].draw(screen, scaled_floor_image, WHITE, button_down)
        for elevator in self.elevators:
            elevator.draw(screen, scaled_elevator_img)


    def allocate_elevator(self, dest):
        """
        Assigns the closest elevator to the requested index.
        Args:
            dest (int): The target index.
        Returns:
            Elevator: The assigned elevator.
        """
        closest = min(self.elevators, key=lambda elevator: elevator.closest(dest))
        closest.queue.append(dest)
        closest.occupied_time += STOP_TIME + time_by_distance(closest.final, dest)
        closest.final = dest
        return closest


    def is_floor_called(self, dest):
        """
        Checks if any elevator is already assigned to the requested index.
        Args:
            dest (int): The target index.
        Returns:
            bool: True if an elevator is assigned, False otherwise.
        """
        if any(dest in elevator.queue
               or dest == elevator.current_dest
               for elevator in self.elevators):
            return True


    def elevator_on_floor(self, level):
        """
        Updates the floor when an elevator arrives and performs necessary actions.
        Args:
            level (int): The index of the arrived floor.
        """
        for floor in self.floors:
            if floor.top_left[1] + FLOOR_SPACER_HEIGHT == level:
                floor.button_color = RED
                floor.timer = 0.0


    def update(self, pos):
        """
        Handles floor button presses and updates elevator states.
        Args:
            pos (tuple): The (x, y) coordinates of the click event.
        """
        if pos:
            x, y = pos
            for floor in self.floors:
                level = floor.button_pressed(x, y)
                if level is not None:
                    _, dest_y = floor.top_left
                    floor.pushed_button = True
                    dest = dest_y + FLOOR_SPACER_HEIGHT
                    if not self.is_floor_called(dest):
                        elevator = self.allocate_elevator(dest)
                        floor.button_color = GREEN
                        floor.timer = elevator.occupied_time - STOP_TIME

        for elevator in self.elevators:
            elevator.update()




