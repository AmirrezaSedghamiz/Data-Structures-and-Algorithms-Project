import os

class Penalty:
    def __init__(self, penalty_id : int, driver_id : int, plate_number : str,
                 penalty_date : str , penalty_level : str, description : str) -> None:
        self.penalty_id : int = penalty_id
        self.driver_id : int = driver_id
        self.plate_number : str = plate_number
        self.penalty_date : str = penalty_date
        self.penalty_level : str = penalty_level
        self.description : str = description

    def __str__(self) -> str:
        return (f"Penalty ID: {self.penalty_id}\n"
                f"Driver ID: {self.driver_id}\n"
                f"Plate Number: {self.plate_number}\n"
                f"Penalty Date: {self.penalty_date}\n"
                f"Penalty Level: {self.penalty_level}\n"
                f"Description: {self.description}")

    def save_penalties_to_file(self, directory: str = "InitialData",
                               filename: str = "penalties.txt") -> None:
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, filename)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write("PenaltyID | DriverID | PlateNumber | PenaltyDate | PenaltyLevel | Description\n")
            line = f"{self.penalty_id} | {self.driver_id} | {self.plate_number} | {self.penalty_date} | {self.penalty_level} | {self.description}"
            file.write(line + "\n")
