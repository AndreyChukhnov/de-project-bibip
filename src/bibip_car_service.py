from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
from decimal import Decimal
from datetime import datetime
import os

# Инициируем класс индексов для таблицы models
class ModelIndex:
     def __init__(self, model_id: int, position_in_file_models: int):
        self.model_id = model_id
        self.position_in_file_models = position_in_file_models

# Инициируем класс индексов для таблицы cars
class CarIndex:
    def __init__(self, car_id: str, position_in_file_cars: int):
        self.car_id = car_id
        self.position_in_file_cars = position_in_file_cars

# Инимциируем клас нидексов для таблицы sales
class SaleIndex:
    def __init__(self, sale_id:str, position_in_file_sales: int):
        self.sale_id = sale_id
        self.position_in_file_sales = position_in_file_sales

"""_summary_
"""
class CarService:
    def _format_path(self, filename: str) -> str:
        """Объединяет root_directory_path и имя файла для получения полного пути"""
        return os.path.join(self.root_directory_path, filename)
    
    def _read_file(self, filename: str) -> list[list[str]]:
        """Читает файл и формирует список списков строк"""
        if not os.path.exists(self._format_path(filename)):
            return []
        else:
            with open(self._format_path(filename), 'r', encoding='utf-8') as f:
                lines = f.readlines()
                split_lines = [l.strip().split(',') for l in lines]
                return split_lines
            
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path
        self.model_index: list[ModelIndex] = []
        self.car_index: list[CarIndex] = []
        self.sale_index:list[SaleIndex] = []

        split_model_lines = self._read_file("models_index.txt")
        self.model_index = [ModelIndex(int(l[0]), int(l[1])) for l in split_model_lines]

        split_car_lines = self._read_file('cars_index.txt')
        self.car_index = [CarIndex(str(l[0]), int(l[1])) for l in split_car_lines]

        split_sales_lines = self._read_file('sales_index.txt')
        self.sale_index = [SaleIndex(str(l[0]), int(l[1])) for l in split_sales_lines]

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        # открываем файл  models на добавление строк и формируем строки из атрибутов класса Model
        with open(self._format_path('models.txt'), 'a') as f:
            str_model = f'{model.id},{model.name},{model.brand}'.ljust(500) + '\n'
            f.write(str_model)

        new_mi = ModelIndex(model.id, len(self.model_index))
        
        self.model_index.append(new_mi)
        self.model_index.sort(key=lambda x: x.model_id)

        with open(self._format_path("models_index.txt"), "w") as f:
            for current_mi in self.model_index:
                str_model = f"{current_mi.model_id},{current_mi.position_in_file_models}".ljust(50)
                f.write(str_model + "\n")
        
        return model

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        with open(self._format_path("cars.txt"), "a") as f:
            str_model = f"{car.vin},{car.model},{car.price},{car.date_start},{car.status}".ljust(500)
            f.write(str_model + "\n")

        new_ci = CarIndex(car.vin, len(self.car_index))

        self.car_index.append(new_ci)
        self.car_index.sort(key=lambda x: x.car_id)

        with open(self._format_path("cars_index.txt"), "w") as f:
            for current_mi in self.car_index:
                str_car = f"{current_mi.car_id},{current_mi.position_in_file_cars}".ljust(50)
                f.write(str_car + "\n")

        return car

    # Задание 2. Сохранение продаж.

    def sell_car(self, sale: Sale) -> Car:
        # Сохранение продаж в файл 'sales.txt'
        with open(self._format_path('sales.txt'), 'a', encoding='utf-8') as sales_file:
            sales_string = f'{sale.sales_number},{sale.car_vin},{sale.sales_date},{sale.cost}'.ljust(500)
            sales_file.write(sales_string + '\n')
        # Сохранение индексов в файл sales_index.txt
        new_si = SaleIndex(sale_id=sale.car_vin, position_in_file_sales=len(self.sale_index))

        self.sale_index.append(new_si)
        self.sale_index.sort(key=lambda x: x.sale_id)

        with open(self._format_path('sales_index.txt'), 'w', encoding='utf-8') as index_file:
           for element in self.sale_index:
               string = f'{element.sale_id},{element.position_in_file_sales}'.ljust(50)
               index_file.write(string + '\n')
        
            

    # Задание 3. Доступные к продаже
    """ Метод для определиния списка доступных к продаже машин """
    def get_cars(self, status: CarStatus) -> list[Car]:
       with open(self._format_path('cars.txt'), 'r') as car_file:
           car_lines: list[str] = car_file.readlines()
           car_line_split = [line.strip().split(',') for line in car_lines]
           return [
               Car(
                    vin=string[0],
                    model=int(string[1]),
                    price=Decimal(string[2]),
                    date_start=datetime.strptime(string[3], "%Y-%m-%d %H:%M:%S"),
                    status=CarStatus(string[4])
                )
                   for string in car_line_split if string[4] == status
           ]

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        # with open(self._format_path('cars_index.txt'), 'r') as index_file:
        #     lines: list[str] = index_file.readlines()

        # target_line = -1
        # for line in lines:
        #     car_id, line_number = line.strip().split(',')
        #     if car_id == vin:
        #         target_line = int(line_number)
        #         break
        # if target_line == -1:
        #     return None
        # print(target_line)
        raise NotImplementedError
            

            

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
        raise NotImplementedError

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        raise NotImplementedError

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        raise NotImplementedError
