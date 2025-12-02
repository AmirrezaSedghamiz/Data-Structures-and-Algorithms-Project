from datetime import date
from Design.Car import Car


class SellHistory:
    def __init__(self, sell_id : int , car : Car , buyer_id : int , buy_time : str , expire_time : str | None) -> None :
        self.sell_id : int = sell_id
        self.car : Car = car
        self.buyer_id : int = buyer_id
        self.buying_time : str = buy_time
        self.selling_time : str | None = expire_time

    def __str__(self) -> str:
        return (f"Sell ID: {self.sell_id}\n"
                f"Car: {self.car.car_id}\n"
                f"Buyer ID: {self.buyer_id}\n"
                f"Buying Time: {self.buying_time}\n"
                f"Selling Time: {self.selling_time if self.selling_time is not None else 'Not sold yet'}")
