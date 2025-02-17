from building import *
from config import *
import pygame


def time_by_distance(y1, y2):
    distance = y1 - y2
    return (abs(distance) / FLOOR_HEIGHT) * FLOOR_TRANSIT_TIME


class Elevator:
    def __init__(self, serial_number, building):
        self.queue = []
        # self.__index_default_location = lambda default_location: \
        #     (math.floor(BUILDING_HEIGHT / (NUM_OF_ELEVATORS + 1) * serial_number))
        self.serial_number = serial_number
        self.occupied_time = 0
        self.status = False
        self.y = None
        self.current_dest = None
        self.arrived_time = None
        self.final = None
        self.last_update = None
        self.wait_start_time = None
        self.my_building = building

    def draw(self, screen, image):
        width, height = image.get_size()
        screen.blit(image, (MARGIN * 2 + FLOOR_WIDTH + self.serial_number * (width + MARGIN), self.y))

    def closest(self, y):
        return self.occupied_time + time_by_distance(self.final, y)

    def config_task(self):
        if not self.status and self.queue:
            self.current_dest = self.queue.pop(0)
            self.last_update = pygame.time.get_ticks()
            self.status = "on move"
            print(f"Elevator {self.status}")

    def elapsed_time(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_update
        self.last_update = current_time
        return elapsed_time, current_time

    def stop_time_passed(self):
        elapsed_time, current_time = self.elapsed_time()
        delta_time = current_time - self.arrived_time
        self.occupied_time -= min(self.occupied_time, elapsed_time)
        if delta_time >= STOP_TIME:
            return True

    def update(self):
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
            
            

    # def end_point(self):
    #     if self.in_use:
    #         return self.queue[-1] if self.queue else current_call
    #     return self.default_location









