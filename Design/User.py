import random
from datetime import datetime, date
from Design.Car import Plate, generate_plate_number, Car
from Design.Penalty import Penalty


class User :
    def __init__(self , firstname : str , lastname : str , user_id : int , password : str , date_of_birth : str) -> None:
        self.firstname : str = firstname
        self.lastname : str = lastname
        self.id : int = user_id
        self.key : str = "A"
        self .password : str = password
        self.date_of_birth : str = date_of_birth
        self.penalty_days : int = 0

    def __str__(self) -> str:
        return (f"User(ID: {self.id}, Name: {self.firstname} {self.lastname}, "
                f"Password: {self.password}, Date of Birth: {self.date_of_birth})")

    def isValidLogin(self, user_id : int ,password : str) -> bool:
        return user_id == self.id and password == self.password

    def has_letters_and_digits(self, password : str):
        has_digit = any(char.isdigit() for char in password)
        has_alpha = any(char.isalpha() for char in password)
        return has_digit and has_alpha

    def isValidPassword(self, password : str) -> bool:
        return len(password) == 8 and self.has_letters_and_digits(password)

    def generatePlate(self, car_id: int, cityCode : str , handler):
        while True:
            plate_number :str = generate_plate_number(city_code=cityCode)
            selectedPlate : Plate | None = None
            for plate in handler.plate_history:
                if plate.plate_number == plate_number:
                    selectedPlate = plate
                    break
            if selectedPlate is None :
                print(plate_number)
                break
            elif datetime.strptime(selectedPlate.end_date, "%Y-%m-%d").date() < datetime.today().date() :
                print(plate_number)
                break
        today = date.today()
        today_str : str = today.strftime("%Y-%m-%d")
        hundred_years_later = today.replace(year=today.year + 100)
        later_str : str = hundred_years_later.strftime("%Y-%m-%d")
        return Plate(plate_number,car_id, self.id, today_str, later_str)


class Driver :
    def __init__(self, user_id : int , driver_id : int , license_date : str) -> None:
        self.id: int = user_id
        self.driver_id: int = driver_id
        self.license_date : str = license_date
        self.is_authorized = True

    def __str__(self) -> str:
        return (f"Driver(User ID: {self.id}, Driver ID: {self.driver_id}, "
                f"License Date: {self.license_date}, Block Status: {not self.is_authorized})")


class Driver_Phase_4 :
    def __init__(self, user_id : int , driver_id : int , negative_points : int) -> None:
        self.id: int = user_id
        self.driver_id: int = driver_id
        self.negative_points: int = negative_points

    def __str__(self) -> str:
        return (f"Driver(User ID: {self.id}, Driver ID: {self.driver_id}, "
                f"License Date: {self.negative_points})")

    def add_negative_points(self, number : int, car : Car , penalty_level : str, handler) -> None:
        self.negative_points += number
        if self.negative_points > 500 :
            driver : Driver = handler.drivers.search(Driver(self.id, self.driver_id, ""))
            driver.is_authorized = False
        user : User = handler.users.search(User("", "", self.id, "", ""))
        user.penalty_days = self.negative_points//10
        today = date.today()
        today_str: str = today.strftime("%Y-%m-%d")
        description : str = input("Enter the description : ")
        penalty : Penalty = Penalty(random.randint(100000, 999999), self.driver_id, car.plate_number,
                                    today_str, penalty_level, description)
        handler.penalties.insert(penalty)
        penalty.save_penalties_to_file()
        print("Successfully added")

    def add_penalty(self, penalty_level : str, car : Car, handler) -> None:
        if penalty_level == "Low" :
            self.add_negative_points(10 , car, penalty_level ,handler)
        elif penalty_level == "Medium" :
            self.add_negative_points(30, car, penalty_level, handler)
        elif penalty_level == "High" :
            self.add_negative_points(50, car, penalty_level, handler)
        else:
            print("Invalid Penalty Level")


