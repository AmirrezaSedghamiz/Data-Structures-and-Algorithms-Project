import os
import random

from DataStructures.AVL import AVLTree
from DataStructures.LinkedList import LinkedList
from Design.Car import Plate, Car, Color
from Design.City import City
from Design.Manager import Manager
from Design.SellHistory import SellHistory
from Design.User import User, Driver, Driver_Phase_4
from Design.Penalty import Penalty


class Handler:
    def __init__(self):
        self.cityCodes: LinkedList[City] = LinkedList[City](equals_func=lambda c1, c2: c1.name == c2.name)
        self.users: AVLTree[User] = AVLTree[User](key_func=lambda user: user.id)
        self.cars: AVLTree[Car] = AVLTree[Car](key_func=lambda car: car.car_id)
        self.plate_history: AVLTree[Plate] = AVLTree[Plate](key_func=lambda plate: plate.plate_number)
        self.drivers: AVLTree[Driver] = AVLTree[Driver](key_func=lambda driver: driver.driver_id)
        self.penalties: AVLTree[Penalty] = AVLTree[Penalty](key_func=lambda penalty: penalty.penalty_id)
        self.sell_history: AVLTree[SellHistory] = AVLTree[SellHistory](key_func=lambda sell: sell.sell_id)
        self.driver_negative_points: AVLTree[Driver_Phase_4] = AVLTree[Driver_Phase_4](
            key_func=lambda driver: driver.driver_id)
        self.manager : Manager = Manager(12345,"admin")

    def initialize(self):
        self._load_users()
        self._load_cars()
        self._load_drivers()
        self._load_phase4_drivers()
        self._load_penalties()
        self._load_plate_history()
        self._load_cities()

    def _load_users(self):
        file_path = os.path.join(os.getcwd(), "InitialData", "users.txt")
        with open(file_path, "r", encoding="utf-8") as file:
            next(file)
            for line in file:
                parts = [p.strip() for p in line.strip().split("|")]
                if len(parts) != 5:
                    continue
                user_id = int(parts[0])
                firstname = parts[1]
                lastname = parts[2]
                date_of_birth = parts[3]
                password = parts[4]

                user = User(firstname, lastname, user_id, password, date_of_birth)
                self.users.insert(user)

    def _load_cars(self):
        file_path = os.path.join(os.getcwd(), "InitialData", "cars.txt")
        with open(file_path, "r", encoding="utf-8") as file:
            next(file)
            for line in file:
                parts = [p.strip() for p in line.strip().split("|")]
                if len(parts) != 6:
                    continue
                car_id = int(parts[0])
                name = parts[1]
                production_date = parts[2]
                plate_number = parts[3]
                color_str = parts[4]
                user_id = int(parts[5])

                try:
                    color = Color[color_str]
                except KeyError:
                    color = Color.OT

                car = Car(name, production_date, car_id, color, user_id, plate_number)
                new_sell_history: SellHistory = SellHistory(random.randint(1, 100000), car,
                                                            car.user_id, car.production_date , None)
                self.sell_history.insert(new_sell_history)
                self.cars.insert(car)

    def _load_drivers(self):
        file_path = os.path.join(os.getcwd(), "InitialData", "drivers.txt")
        with open(file_path, "r", encoding="utf-8") as file:
            next(file)
            for line in file:
                parts = [p.strip() for p in line.strip().split("|")]
                if len(parts) != 3:
                    continue
                user_id = int(parts[0])
                driver_id = int(parts[1])
                license_date = parts[2]

                driver = Driver(user_id, driver_id, license_date)
                self.drivers.insert(driver)

    def _load_phase4_drivers(self):
        file_path = os.path.join(os.getcwd(), "InitialData", "phase4.txt")
        with open(file_path, "r", encoding="utf-8") as file:
            next(file)
            for line in file:
                parts = [p.strip() for p in line.strip().split("|")]
                if len(parts) != 3:
                    continue
                user_id = int(parts[0])
                driver_id = int(parts[1])
                negative_points = int(parts[2])

                driver_phase4 = Driver_Phase_4(user_id, driver_id, negative_points)
                self.driver_negative_points.insert(driver_phase4)

    def _load_penalties(self):
        file_path = os.path.join(os.getcwd(), "InitialData", "penalties.txt")
        with open(file_path, "r", encoding="utf-8") as file:
            next(file)
            for line in file:
                parts = [p.strip() for p in line.strip().split("|")]
                if len(parts) != 6:
                    continue
                penalty_id = int(parts[0])
                driver_id = int(parts[1])
                plate_number = parts[2]
                penalty_date = parts[3]
                penalty_level = parts[4]
                description = parts[5]

                penalty = Penalty(penalty_id, driver_id, plate_number, penalty_date, penalty_level, description)
                self.penalties.insert(penalty)

    def _load_plate_history(self):
        file_path = os.path.join(os.getcwd(), "InitialData", "ownership_history.txt")
        with open(file_path, "r", encoding="utf-8") as file:
            next(file)
            for line in file:
                parts = [p.strip() for p in line.strip().split("|")]
                if len(parts) != 5:
                    continue
                car_id = int(parts[0])
                user_id = int(parts[1])
                start_date = parts[2]
                end_date = parts[3]
                plate_number = parts[4]

                plate = Plate(plate_number, car_id, user_id, start_date, end_date)
                self.plate_history.insert(plate)

    def _load_cities(self):
        file_path = os.path.join(os.getcwd(), "InitialData", "citycode.txt")
        with open(file_path, "r", encoding="utf-8") as file:
            next(file)
            for line in file:
                parts = [p.strip() for p in line.strip().split("|")]
                if len(parts) != 2:
                    continue
                code = parts[0]
                name = parts[1]

                city = City(name, code)
                self.cityCodes.insert_at_tail(city)

