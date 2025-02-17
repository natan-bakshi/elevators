from elevator import *
from floor import *


class Building:
    def __init__(self, num_of_floors, num_of_elevators, screen):
        self.floors = [Floor(i) for i in range(num_of_floors)]
        self.elevators = [Elevator(i, self) for i in range(num_of_elevators)]
        for elevator in self.elevators:
            elevator.y = elevator.final = screen.get_height() - MARGIN - FLOOR_HEIGHT + FLOOR_SPACER_HEIGHT

    def draw(self, screen, button_down=None):
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
        closest = min(self.elevators, key=lambda elevator: elevator.closest(dest))
        closest.queue.append(dest)
        closest.occupied_time += STOP_TIME + time_by_distance(closest.final, dest)
        closest.final = dest
        return closest

    def is_floor_called(self, dest):
        if any(dest in elevator.queue
               or dest == elevator.current_dest
               for elevator in self.elevators):
            return True

    def elevator_on_floor(self, level):
        for floor in self.floors:
            if floor.top_left[1] + FLOOR_SPACER_HEIGHT == level:
                floor.button_color = RED
                floor.timer = 0.0

    def update(self, pos):
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




        # # base_distance =
        # closest = min(elevator.occupancy_time + 2000 + time_by_distance(elevator.queue[-1], y) for elevator in self.elevators)

