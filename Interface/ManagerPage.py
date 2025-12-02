import os
import random
from datetime import datetime

from DataStructures.LinkedList import LinkedList
from DataStructures.Stack import Stack
from Design.Car import Car, Color, isValidPlateNumber, Plate
from Design.City import City
from Design.Penalty import Penalty
from Design.SellHistory import SellHistory
from Design.User import User, Driver, Driver_Phase_4
from Repository.Handler import Handler
from Design.Manager import Manager


class ManagerPage:
    def __init__(self, handler: Handler, manager: Manager ,stack : Stack):
        self.handler: Handler = handler
        self.manager: Manager = manager
        self.stack: Stack = stack

    def showPage(self):
        try:
            print("Welcome Manager !\n")
            print("0.Exit\n1.back to login\n2.add car\n3.log all cars\n4.log all users\n5.log plates by city"
                  "\n6.log cars by city\n7.log cars by production date\n8.log car owners by city"
                  "\n9.change user name\n10.log all drivers\n11.delete car\n12.grant driver privilege"
                  "\n13.delete driver\n14.change driver authority\n15.add penalty\n16.change ownership"
                  "\n17.log all sell history\n18.log all sell history for car\n19.display driver ranking\n")
            action : int = int(input("Enter your action : "))
            if action == 0:
                print("Goodbye. See you soon!")
                exit(0)
            elif action == 1:
                self.stack.pop()
            elif action == 2:
                self.add_car()
            elif action == 3:
                self.log_all_cars()
            elif action == 4:
                self.log_all_users()
            elif action == 5:
                self.log_plates_by_city()
            elif action == 6:
                self.log_cars_by_city()
            elif action == 7:
                self.log_cars_by_production_date()
            elif action == 8:
                self.log_car_owners_by_city()
            elif action == 9:
                self.change_user_name()
            elif action == 10:
                self.log_all_drivers()
            elif action == 11:
                self.delete_car()
            elif action == 12:
                self.grant_driver_privilege()
            elif action == 13:
                self.delete_driver_cascade()
            elif action == 14:
                self.change_drivers_authority()
            elif action == 15:
                self.add_penalty()
            elif action == 16:
                self.change_ownership()
            elif action == 17:
                self.log_all_sell_history()
            elif action == 18:
                self.log_all_sell_history_for_car()
            elif action == 19:
                self.display_driver_ranking()
            else:
                print("Invalid Input !")
        except Exception as e:
            print("Invalid Input ! ")

    def log_all_cars(self) -> None:
        for car in self.handler.cars:
            print(str(car))

    def log_all_users(self) -> None:
        for user in self.handler.users:
            print(str(user) + "\n")
            for car in self.handler.cars:
                if car.user_id == user.id:
                    print(str(car))
            print("\n")

    def has_date_passed(self, date_str: str) -> bool:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        today = datetime.today().date()
        return date < today

    def log_plates_by_city(self) -> None:
        city: City = self.handler.cityCodes.search(City(input("What city do you have in mind? "), ""))
        for plate in self.handler.plate_history:
            if plate.city == city.code:
                isBefore = self.has_date_passed(plate.date)
                if isBefore:
                    print("Available : " + str(plate))
                else:
                    print("Unavailable : " + str(plate))

    def log_cars_by_city(self) -> None:
        city: City = self.handler.cityCodes.search(City(input("What city do you have in mind? "), ""))
        for car in self.handler.cars:
            if car.plate_number[-2:] == city.code:
                print(str(car))

    def log_cars_by_production_date(self) -> None:
        date1: str = input("First date do you have in mind? ")
        date2: str = input("Second date do you have in mind? ")
        if date1 == "" and date2 == "":
            for car in self.handler.cars:
                print(str(car))
            return
        elif date1 == "":
            for car in self.handler.cars:
                if datetime.strptime(date2, "%Y-%m-%d").date() < datetime.strptime(car.production_date,
                                                                                   "%Y-%m-%d").date():
                    print(str(car))
            return
        elif date2 == "":
            for car in self.handler.cars:
                if datetime.strptime(date1, "%Y-%m-%d").date() < datetime.strptime(car.production_date,
                                                                                   "%Y-%m-%d").date():
                    print(str(car))
            return
        if datetime.strptime(date1, "%Y-%m-%d").date() > datetime.strptime(date2, "%Y-%m-%d").date():
            print("The second date is larger than the first date!")
            return
        for car in self.handler.cars:
            if datetime.strptime(date1, "%Y-%m-%d").date() < datetime.strptime(car.production_date,
                                                                               "%Y-%m-%d").date() < datetime.strptime(
                    date2, "%Y-%m-%d").date():
                print(str(car))

    def log_car_owners_by_city(self):
        city: City = self.handler.cityCodes.search(City(input("What city do you have in mind? "), ""))
        for car in self.handler.cars:
            if car.plate_number[-2:] == city.code:
                for user in self.handler.users:
                    if user.id == car.user_id:
                        print(str(user))
                        break

    def change_user_name(self) -> None:
        flag : bool = False
        user_id : int = int(input("What is the user's id? "))
        for user in self.handler.users:
            if user.id == user_id:
                flag = True
                user.firstname = input("What is the user's firstname? ")
                user.lastname = input("What is the user's lastname? ")
                file_path = os.path.join(os.path.dirname(__file__), "InitialData", "users.txt")
                with open(file_path, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                header = lines[0]
                updated_lines = [header]
                for line in lines[1:]:
                    parts = [p.strip() for p in line.strip().split("|")]
                    if len(parts) != 5:
                        continue
                    national_id = int(parts[0])
                    if national_id == user_id:
                        parts[1] = user.firstname
                        parts[2] = user.lastname
                        updated_line = " | ".join(parts) + "\n"
                    else:
                        updated_line = " | ".join(parts) + "\n"
                    updated_lines.append(updated_line)
                with open(file_path, "w", encoding="utf-8") as file:
                    file.writelines(updated_lines)
                break
        if not flag:
            print("user not found!")

    def add_car(self) :
        car_id : int = int(input("What is the car's id ? "))
        car_name : str = input("What is the car's name ? ")
        car_plate : str = input("What is the car's plate number ? ")
        color : str = input("What is the car's color ? ")
        production_date : str = input("What is the production date ? ")
        plate_date : str = input("What is the plate's date ? ")
        if not isValidPlateNumber(car_plate):
            print("invalid plate number")
            return
        if (datetime.strptime(production_date, "%Y-%m-%d").date() <
                datetime.strptime(plate_date,"%Y-%m-%d").date()):
            print("Invalid dates entered !")
            return None
        try :
            colored : Color = Color[color]
        except KeyError as e:
            print("Invalid Color ! ")
            return
        user_id : int = int(input("Enter the owner's id : "))
        car : Car = Car(car_name, production_date,car_id, colored, user_id,car_plate)
        self.handler.cars.insert(car)
        original_date = datetime.strptime(plate_date, "%Y-%m-%d")
        future_date = original_date.replace(year=original_date.year + 100)
        result = future_date.strftime("%Y-%m-%d")
        plate : Plate = Plate(car_plate, car_id, user_id, plate_date, result)
        self.handler.plate_history.insert(plate)
        print("Car added successfully ! ")

    def log_all_drivers(self):
        for driver in self.handler.drivers:
            print(str(driver))

    def delete_car(self):
        car_id : int = int(input("Enter the car's id : "))
        for car in self.handler.cars:
            if car.car_id == car_id:
                self.handler.cars.delete(car)
                print("Car deleted")
                return

    def grant_driver_privilege(self):
        user_id : int = int(input("Enter the user's id : "))
        user : User | None = self.handler.users.search(User("", "", user_id , "" ,""))
        if user is None :
            print("User not found ! ")
            return

        def is_at_least_18(birthdate_str: str) -> bool:
            birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")
            today = datetime.today()
            eighteenth_birthday = birthdate.replace(year=birthdate.year + 18)
            try:
                eighteenth_birthday = birthdate.replace(year=birthdate.year + 18)
            except ValueError:
                eighteenth_birthday = birthdate.replace(year=birthdate.year + 18, day=28)

            return today >= eighteenth_birthday

        if not is_at_least_18(user.date_of_birth):
            print("User can't drive because of his age ! ")
            return
        while True:
            driver_id : int = random.randint(10000000, 999999999)
            search : Driver | None = self.handler.drivers.search(Driver(user_id, driver_id, datetime.today().strftime("%Y-%m-%d")))
            if search is not None:
                break
        self.handler.drivers.insert(Driver(user_id, driver_id, datetime.today().strftime("%Y-%m-%d")))
        self.handler.driver_negative_points.insert(Driver_Phase_4(user_id, driver_id, 0))
        print("Successful operation !")

    def delete_driver_cascade(self):
        user_id: int = int(input("Enter the user's id : "))
        search_driver : Driver | None = None
        for driver in self.handler.drivers:
            if driver.user_id == user_id:
                search_driver = driver
                break
        if search_driver is None:
            print("Driver not found ! ")
            return
        penalties : LinkedList[Penalty] = LinkedList[Penalty](equals_func=lambda p1, p2: p1.penalty_id == p2.penalty_id)
        for penalty in self.handler.penalties:
            if penalty.driver_id == search_driver.driver_id:
                penalties.insert_at_tail(penalty)
        for penalty in penalties:
            self.handler.penalties.delete(penalty)
        self.handler.driver_negative_points.delete(Driver_Phase_4(search_driver.id, search_driver.driver_id, 0))
        self.handler.drivers.delete(search_driver)
        print("Driver deleted !")

    def change_drivers_authority(self):
        identifier : int = int(input("Enter the user's id or the driver's id : "))
        for driver in self.handler.drivers:
            if driver.id == identifier or driver.driver_id == identifier:
                action : str = input("Do you want to give him authority ? [Y/N]")
                if action == "Y" :
                    driver.is_authorized = True
                if action == "N" :
                    driver.is_authorized = False
                else :
                    print("Invalid choice")
                return
        print("Driver not found ! ")

    def add_penalty(self):
        driver_id : int = int(input("Enter the driver's id : "))
        searched_driver : Driver_Phase_4 | None = self.handler.driver_negative_points.search(
            Driver_Phase_4(-1 , driver_id, 0)
        )
        if searched_driver is None:
            print("Driver not found !")
            return
        car_id : int = int(input("Enter the car's id : "))
        searched_car : Car | None = self.handler.cars.search(Car("", "",car_id,
                                                                 Color.BC, searched_driver.id, ""))
        if searched_car is None:
            print("Car not found !")
            return
        penalty_level : str = input("Enter the penalty level : [Low/ Medium/High] ")
        searched_driver.add_penalty(penalty_level, searched_car, self.handler)

    def _calculate_and_rank_drivers(self) -> LinkedList[tuple]:
        drivers_data = LinkedList()

        for driver_phase4 in self.handler.driver_negative_points:
            driver = self.handler.drivers.search(Driver(-1, driver_phase4.driver_id, ""))
            if driver:
                drivers_data.insert_at_tail({
                    'driver_id': driver_phase4.driver_id,
                    'negative_points': driver_phase4.negative_points,
                    'license_date': driver.license_date
                })

        ranked_drivers = LinkedList()

        outer_node = drivers_data.head
        while outer_node:
            current_driver = outer_node.data
            score = 0
            inner_node = outer_node.next
            while inner_node:
                other_driver = inner_node.data
                if other_driver['negative_points'] >= current_driver['negative_points']:
                    score += 1
                inner_node = inner_node.next
            ranked_drivers.insert_at_tail((
                current_driver['driver_id'],
                score,
                current_driver['negative_points'],
                current_driver['license_date']
            ))
            outer_node = outer_node.next

        sorted_ranked = LinkedList()
        while not ranked_drivers.is_empty():
            best_node = ranked_drivers.head
            best_prev = None
            current = ranked_drivers.head
            prev = None

            while current:
                if (
                        current.data[1] > best_node.data[1] or
                        (current.data[1] == best_node.data[1] and current.data[3] < best_node.data[3])
                ):
                    best_node = current
                    best_prev = prev
                prev = current
                current = current.next

            if best_prev is None:
                ranked_drivers.head = best_node.next
            else:
                best_prev.next = best_node.next
            if best_node == ranked_drivers.tail:
                ranked_drivers.tail = best_prev
            ranked_drivers._size -= 1

            sorted_ranked.insert_at_tail(best_node.data)

        return sorted_ranked

    def display_driver_ranking(self):
        ranked_drivers = self._calculate_and_rank_drivers()
        print("\nDriver Ranking:")
        print("Rank | Driver ID | Score | Negative Points | License Date")
        print("-" * 60)

        rank = 1
        current = ranked_drivers.head
        while current:
            driver_id, score, negative_points, license_date = current.data
            driver = self.handler.drivers.search(Driver(-1, driver_id, ""))
            user = self.handler.users.search(User("", "", driver.id, "", "")) if driver else None
            name = f"{user.firstname} {user.lastname}" if user else "Unknown"
            print(f"{rank:4} | {driver_id:9} | {score:5} | {negative_points:15} | {license_date:12} | {name}")
            current = current.next
            rank += 1

    def change_ownership(self):
        plate_id : str = input("Enter the plate number or car id : ")
        is_int : bool = False
        try:
            plate_id : int = int(plate_id)
            is_int = True
        except ValueError:
            plate_id : str = plate_id
        searched_car : Car | None = None
        for car in self.handler.cars:
            if is_int and car.car_id == plate_id:
                searched_car = car
                break
            if not is_int and car.plate_number == plate_id:
                searched_car = car
                break
        if not searched_car:
            print("Car not found ! ")
            return
        new_plate_number : str = input("Enter the new plate number : ")
        if not isValidPlateNumber(new_plate_number):
            print("Invalid plate number ! ")
            return
        for car in self.handler.cars:
            if car.plate_number == new_plate_number:
                print("This plate number is taken ! ")
                return
        new_user_id : int = int(input("Enter the new owner's id : "))
        new_user : User | None = None
        for user in self.handler.users:
            if user.id == new_user_id:
                new_user = user
                break
        if not new_user:
            print("User not found ! ")
            return
        searched_plate : Plate | None = None
        for plate in self.handler.plate_history:
            if plate.plate_number == searched_car.plate_number:
                searched_plate = plate
                break
        if not searched_plate:
            print("Bug in the code ! ")
            return
        searched_plate.car_id = -1
        searched_plate.end_date = datetime.today().strftime("%Y-%m-%d")
        original_date = datetime.strptime(datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
        future_date = original_date.replace(year=original_date.year + 100)
        result = future_date.strftime("%Y-%m-%d")
        new_plate : Plate = Plate(new_plate_number,searched_car.car_id,new_user.id,datetime.today().strftime("%Y-%m-%d"),result)
        self.handler.plate_history.insert(new_plate)
        searched_car.plate_number = new_plate_number
        searched_car.user_id = new_user.id
        for sell in self.handler.sell_history:
            if sell.car.car_id == searched_car.car_id and sell.selling_time is None :
                sell.selling_time = datetime.today().strftime("%Y-%m-%d")
                break
        new_sell_history : SellHistory = SellHistory(random.randint(1, 1000000),searched_car ,
                                                     new_user.id,datetime.today().strftime("%Y-%m-%d"), None)
        self.handler.sell_history.insert(new_sell_history)
        print("Successful transaction ! ")

    def log_all_sell_history(self):
        for sell_history in self.handler.sell_history:
            for user in self.handler.users:
                if user.id == sell_history.buyer_id:
                    print("Name : " + user.firstname + " " + user.lastname + " : ")
                    print(str(sell_history))
                    break

    def log_all_sell_history_for_car(self):
        car_id : int = int(input("Enter car id: "))
        searched_car : Car | None = None
        for car in self.handler.cars:
            if car.car_id == car_id:
                searched_car = car
                break
        if searched_car is None:
            print("Car not found ! ")
            return
        for sell_history in self.handler.sell_history:
            if sell_history.car.car_id == searched_car.car_id:
                print(str(sell_history))
