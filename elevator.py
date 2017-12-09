import argparse
import time


def get_args():
    parser = argparse.ArgumentParser(description='elevator emulator')
    parser.add_argument('-fl', '--floors', help='number of floors (5 to 20)', default=10, type=int)
    parser.add_argument('-fh', '--floor_height', help='height of one floor (meters)', default=2.0,
                        type=float)
    parser.add_argument('-s', '--elevator_speed', help='elevator speed (meters/seconds)', default=0.5,
                        type=float)
    parser.add_argument('-d', '--door_time', help='time to open and close doors (seconds)',
                        default=3, type=int)
    args = parser.parse_args()

    return {
        "floors": args.floors,
        "floor_height": args.floor_height,
        "elevator_speed": args.elevator_speed,
        "door_time": args.door_time
    }


class Elevator(object):
    def __init__(self, floors, floor_height, elevator_speed, door_time):
        self.floors = floors
        self.floor_height = floor_height
        self.elevator_speed = elevator_speed
        self.door_time = door_time
        self.current_floor = 1  # always starts at 1st floor
        self.allowed_floors = range(1, self.floors+1)
        self.time_between_floors = self.floor_height /  self.elevator_speed
        print "You have an elevator:\n" \
            "- there are {} floors in your building,\n" \
            "- each floor is {} m,\n" \
            "- elevator moves with speed {} m/sec,\n" \
            "- door open/close time is {} sec,\n" \
            "- your elevator is at floor {}".format(self.floors,
                                                    self.floor_height,
                                                    self.elevator_speed,
                                                    self.door_time,
                                                    self.current_floor)

    def call(self, command_place, new_floor):
        """Waits for a call from User"""
        print "Received command from {}".format(command_place)
        if new_floor in self.allowed_floors and (new_floor != self.current_floor):
            print "Ok, moving to the floor {}".format(new_floor)
        else:
            print "Dude, that floor doesn't exist! Try one more time."
            return

        delta = self.current_floor - new_floor
        if delta > 0:
            self.move_down(delta)
        elif delta < 0:
            self.move_up(delta)
        else:
            print "Are you sure, you want to stay at {} floor?".format(self.current_floor)

    def move_up(self, delta):
        for i in range(abs(delta)):
            time.sleep(self.time_between_floors)
            self.current_floor += 1
            print "Elevator is at {} floor".format(self.current_floor)
        self.open_close_door()

    def move_down(self, delta):
        for i in range(delta):
            time.sleep(self.time_between_floors)
            self.current_floor -= 1
            print "Elevator is at {} floor".format(self.current_floor)
        self.open_close_door()

    def open_close_door(self):
        print "Opening doors"
        time.sleep(self.door_time / 4)
        print "Doors are opened"
        time.sleep(self.door_time / 2)
        print "Closing doors"
        time.sleep(self.door_time / 4)
        print "Doors are closed"

if __name__ == '__main__':
    args = get_args()
    elevator = Elevator(args["floors"], args["floor_height"],
                        args["elevator_speed"], args["door_time"])

    while True:
        raw = raw_input("Please input in/out + floor number you want, separated by space (Example: in 7). \n")
        raw = raw.strip()
        raw_split = raw.split(" ")
        if len(raw_split) == 2:
            try:
                command_place = str(raw_split[0])
                floor = int(raw_split[1])
                elevator.call(command_place, floor)
            except Exception as e:
                print "Wrong input! Problems with {}\n".format(e)
                pass
        else:
            pass
