import os
import string
from enum import Enum
import re
import random


class Color(Enum):
    WT = 0
    BC = 1
    RD = 2
    BL = 3
    GR = 4
    OT = 5

    def __str__(self):
        names = {
            Color.WT: "White",
            Color.BC: "Black",
            Color.RD: "Red",
            Color.BL: "Blue",
            Color.GR: "Green",
            Color.OT: "Other"
        }
        return names.get(self, "Unknown")


class Car:
    def __init__(self, name : str, production_date : str , car_id : int , color : Color, user_id : int ,
                 plate_number : str) -> None:
        self.name : str = name
        self.production_date : str = production_date
        self.car_id : int = car_id
        self.color : Color = color
        self.user_id : int = user_id
        self.plate_number : str = plate_number

    def __str__(self) -> str:
        return (f"Car(Name: {self.name}, Production Date: {self.production_date}, ID: {self.car_id}, "
                f"Color: {str(self.color)}, User ID: {self.user_id}, Plate Number: {self.plate_number})")

class Plate:
    def __init__(self, plate_number : str , car_id : int , user_id : int , start_date : str, end_date : str) -> None:
        self.plate_number : str = plate_number
        self.car_id : int = car_id
        self.city_code : str = plate_number[-2:]
        self.user_id : int = user_id
        self.start_date : str = start_date
        self.end_date : str = end_date

    def __str__(self) -> str:
        return (
            f"Plate Number: {self.plate_number}, "
            f"City Code: {self.city_code}, "
            f"Car ID: {self.car_id}, "
            f"User ID: {self.user_id}, "
            f"Start Date: {self.start_date}, "
            f"End Date: {self.end_date}"
        )

    def save_plates_to_file(self, directory: str = "InitialData",
                            filename: str = "ownership_history.txt") -> None:
        # Ensure the directory exists
        os.makedirs(directory, exist_ok=True)

        file_path = os.path.join(directory, filename)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write("CarID | OwnerNationalID | StartDate | EndDate | PlateNumber\n")
            plate = self
            formatted_line = f"{plate.car_id} | {plate.user_id} | {plate.start_date} | {plate.end_date} | {plate.plate_number}"
            file.write(formatted_line + "\n")


def isValidPlateNumber(plate: str) -> bool:
    if not isinstance(plate, str) or len(plate) != 9 or plate[7] != '-':
        return False
    pattern = r'^(\d{2})([A-Z])(\d{3})-(\d{2})$'
    match = re.match(pattern, plate)
    if not match:
        return False
    prefix, letter, middle, city = match.groups()
    digits = prefix + middle

    if len(set(digits)) == 1:
        return False
    ascending = ''.join(sorted(digits))
    descending = ''.join(sorted(digits, reverse=True))
    if digits == ascending or digits == descending:
        return False
    if letter in ['P', 'D']:
        return False
    if letter == 'X' and any(int(d) % 2 == 0 for d in digits):
        return False
    return True


def generate_plate_number(city_code : str) -> str:
    while True:
        prefix = f"{random.randint(0, 9)}{random.randint(0, 9)}"
        middle = f"{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"
        letter = random.choice([c for c in string.ascii_uppercase if c not in ['P', 'D']])
        digits = prefix + middle
        if letter == 'X':
            digits = ''.join(random.choice('13579') for _ in range(5))
            prefix, middle = digits[:2], digits[2:]

        plate = f"{prefix}{letter}{middle}-{city_code}"

        if isValidPlateNumber(plate):
            return plate
