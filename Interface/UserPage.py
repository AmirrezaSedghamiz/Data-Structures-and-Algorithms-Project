from DataStructures.Stack import Stack
from Design.Car import Car, Color, Plate
from Design.City import City
from Repository.Handler import Handler
from Design.User import User, Driver


class UserPage:
    def __init__(self, handler: Handler , user : User, is_driver : bool, driver: Driver | None , stack : Stack) -> None:
        self.handler : Handler = handler
        self.user : User = user
        self.is_driver : bool = is_driver
        self.driver : Driver | None = driver
        self.stack : Stack = stack

    def showPage(self):
        try:
            if self.is_driver:
                print("Welcome Driver !\n")
            else:
                print("Welcome User !\n")
            print("0.Exit\n1.back to login\n2.generate plate by city\n3.log all cars of user\n"
                  "4.log all plates of user\n"
                  "5.log all plate penalties\n6.log plate history")
            if self.is_driver:
                print("7.log negative points\n8.log all driver penalties")
            action : int = int(input("Enter your action : "))
            if action == 0:
                print("Goodbye. See you soon!")
                exit(0)
            elif action == 1:
                self.stack.pop()
            elif action == 2:
                self.gen_plate_by_city()
            elif action == 3:
                self.log_all_cars_of_user()
            elif action == 4:
                self.log_all_plates_of_user()
            elif action == 5:
                self.log_all_plate_penalties()
            elif action == 6:
                self.log_plate()
            elif action == 7 and self.is_driver:
                self.log_negative_points()
            elif action == 8 and self.is_driver:
                self.log_all_driver_penalties()
            else :
                print("Invalid Input !")
        except Exception as e:
            print("Invalid Input ! ")

    def gen_plate_by_city(self) -> str | None:
        if self.user.penalty_days > 0 :
            print(f"You can't generate a plate number for another {self.user.penalty_days} days")
            return None
        city_name = input("Enter your city's name : ")
        city = self.handler.cityCodes.search(City(city_name, ""))
        if city is None:
            print("This city was not found.")
            return None
        car_id : int = int(input("Enter your car's id : "))
        searched_car : Car | None = (
            self.handler.cars.search(Car("", "", car_id, Color.BC, self.user.id, "")))
        if searched_car is None:
            print("This car was not found.")
            return None
        if searched_car.user_id != self.user.id :
            print("This car doesn't belong to you!")
            return None
        plate : Plate = self.user.generatePlate(searched_car.car_id, city.code, self.handler)
        self.handler.plate_history.insert(plate)
        searched_car.plate_number = plate.plate_number
        plate.save_plates_to_file()

    def log_all_cars_of_user(self) -> None:
        flag: bool = False
        for car in self.handler.cars:
            if car.user_id == self.user.id:
                flag = True
                print(str(car))
        if flag is False:
            print("No cars were found.")

    def log_all_plates_of_user(self) -> None:
        flag : bool = False
        for plate in self.handler.plate_history:
            if plate.user_id == self.user.id:
                flag = True
                print(str(plate))
        if flag is False:
            print("No plates were found.")

    def log_negative_points(self):
        for driver in self.handler.driver_negative_points:
            if driver.id == self.user.id:
                print("Negative points : " , end="")
                print(driver.negative_points)
                return

    def log_all_driver_penalties(self):
        flag : bool = False
        for penalty in self.handler.penalties:
            if penalty.driver_id == self.driver.driver_id:
                flag = True
                print(str(penalty))
        if flag is False:
            print("No penalty found!")

    def log_all_plate_penalties(self):
        plate_number : str = input("Enter your plate number : ")
        flag : bool = False
        for plate in self.handler.plate_history:
            if plate.plate_number == plate_number and plate.user_id == self.user.id:
                flag = True
                break
        if flag is False:
            print("This plate doesn't exist or doesn't belong to you!")
            return None
        flag = False
        for penalty in self.handler.penalties:
            if penalty.plate_number == plate_number:
                flag = True
                print(str(penalty))
        if flag is False:
            print("No penalty found!")

    def log_plate(self):
        plate_number: str = input("Enter your plate number : ")
        flag : bool = False
        for plate in self.handler.plate_history:
            if plate.plate_number == plate_number:
                flag = True
                print(str(plate))
                break
        if flag is False:
            print("No plate found!")


