from building import *
from config import *
import pygame


def time_by_distance(y1, y2):
    """
    Calculates the travel time between two positions.
    Args:
        y1 (int): Starting position.
        y2 (int): Target position.
    Returns:
        float: Estimated travel time.
    """
    distance = y1 - y2
    return (abs(distance) / FLOOR_HEIGHT) * FLOOR_TRANSIT_TIME


class Elevator:
    """ Represents an elevator in the building. """
    def __init__(self, serial_number, building):
        self.queue = []  # The list of tasks assigned to the elevator.
        self.serial_number = serial_number  # The unique identifier of the elevator.
        self.occupied_time = 0  # The time the elevator will remain occupied.
        self.status = False  # Indicates whether the elevator is currently in use.
        self.y = None  # The current index position of the elevator.
        self.current_dest = None  # The current target floor of the elevator.
        self.arrived_time = None  # The time at which the elevator reached a floor.
        self.final = None  # The last task in the queue.
        self.last_update = None  # The last time the display was updated.
        self.my_building = building  # The building instance the elevator belongs to.


    def draw(self, screen, image):
        """
       Draws the elevator on the screen.
       Args:
           screen (pygame.Surface): The surface to draw on.
           image (pygame.Surface): The image representing the elevator.
       The elevator's position is determined by its serial number and its
       real-time index position (`self.y`).
       """
        width, height = image.get_size()
        screen.blit(image, (MARGIN * 2 + FLOOR_WIDTH + self.serial_number * (width + MARGIN), self.y))


    def closest(self, y):
        """
        Returns the estimated time to reach the target position.
        Args:
            y (int): Target position.
        Returns:
            float: Estimated arrival time.
        """
        return self.occupied_time + time_by_distance(self.final, y)


    def config_task(self):
        """
        Assigns the next task from the queue if the elevator is idle.
        Updates the destination, status, and last update time.
        """
        if not self.status and self.queue:
            self.current_dest = self.queue.pop(0)
            self.last_update = pygame.time.get_ticks()
            self.status = "on move"
            print(f"Elevator {self.status}")


    def elapsed_time(self):
        """
        Returns the time elapsed since the last update and updates the timestamp.
        Returns:
            tuple: (elapsed time in milliseconds, current timestamp).
        """
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_update
        self.last_update = current_time
        return elapsed_time, current_time


    def stop_time_passed(self):
        """
        Checks if the elevator's stop time has passed.
        Returns:
            bool: True if the stop time has elapsed, otherwise False.
        """
        elapsed_time, current_time = self.elapsed_time()
        delta_time = current_time - self.arrived_time
        self.occupied_time -= min(self.occupied_time, elapsed_time)
        if delta_time >= STOP_TIME:
            return True


    def update(self):
        """
        Updates the elevator's state, moving it if needed.
        Handles movement, stopping, and task management.
        """
        self.config_task()
        if self.status == "on move":
            if self.y != self.current_dest:
                elapsed_time, current_time = self.elapsed_time()
                pixels_to_travel = round(PIXELS_TRAVELLED_PER_MILLISECOND * elapsed_time)
                direction = 1 if self.current_dest > self.y else -1
                self.y += direction * min(int(pixels_to_travel), abs(self.current_dest - self.y))
                self.occupied_time -= elapsed_time
            else:  # waiting 2 seconds
                self.status = "in stop time"
                print(f"Elevator {self.status}")
                pygame.mixer.music.play()
                self.arrived_time = pygame.time.get_ticks()
                self.my_building.elevator_on_floor(self.current_dest)
        if self.status == "in stop time":
            if self.stop_time_passed():
                self.status = False
                self.last_update = None
            



