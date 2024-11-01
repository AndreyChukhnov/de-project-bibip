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
        
        # читаем индекс
        with open(self._format_path('cars_index.txt'), 'r', encoding='utf-8') as index_file:
            ci_string: list[str] = index_file.readlines()
            target_string = -1
            # print(f"Ищем VIN: {sale.car_vin}")
            for element in ci_string:
                vin, line_number = element.strip().split(',')
                if vin.strip() == sale.car_vin:
                    target_string = int(line_number)
                    # print(f'Найден VIN: {vin}, строка: {line_number}')
                    break
            if target_string == -1:
                raise ValueError('Машина не найдена')

        with open(self._format_path('cars.txt'), 'r+', encoding='utf-8') as car_file:
            car_file.seek(target_string * 502)
            car_line = car_file.readline()
            car_arr = car_line.strip().split(',')
           # print(car_arr)
            car = Car(
                vin=str(car_arr[0]), 
                model=int(car_arr[1]), 
                price = Decimal(car_arr[2]), 
                date_start = datetime.strptime(car_arr[3], "%Y-%m-%d %H:%M:%S"), 
                status=CarStatus(car_arr[4])
                )
            car.status = CarStatus.sold
            car_file.seek(target_string * 502)
            correct_line = f'{car.vin},{car.model},{car.price},{car.date_start},{car.status}'.ljust(500)
            car_file.write(correct_line + '\n')
            # print(car)
            
        return car

            

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
        # Читаем файл с индесами
        with open(self._format_path('cars_index.txt'), 'r') as index_file:
            lines: list[str] = index_file.readlines()

        # Определяем номер строки 
        target_line = -1
        for line in lines:
            car_id, line_number = line.strip().split(',')
            if car_id == vin:
                target_line = int(line_number)
                break
        if target_line == -1:
            return None

        # Читаем строку в файле cars.txt
        with open(self._format_path('cars.txt'), 'r', encoding='utf-8') as car_file:
            car_file.seek(target_line * 502)
            car_line = car_file.readline()
            car_arr = car_line.strip().split(',')
            print(car_arr)

        model_id = int(car_arr[1])

        # Читаем индекс для определения номера строки в файде models.txt
        with open(self._format_path('models_index.txt'), 'r', encoding='utf-8') as mi_file:
            mi_file_lines: list[str] = mi_file.readlines()

        # определяем номер строки в файле models.txt
        model_target_line = -1
        for line in mi_file_lines:
            m_id, line_number = line.strip().split(',')
            if model_id == int(m_id):
                model_target_line = int(line_number)
                break
        if model_target_line == -1:
            raise ValueError('Неправильный VIN')
        
        # Читаем cnhjre d файлt models.txt
        with open(self._format_path('models.txt'), 'r', encoding='utf-8') as model_file:
            model_file.seek(model_target_line * 502)
            model_line = model_file.readline()
            model_arr = model_line.strip().split(',')
            print(model_arr)
        
        if  str(car_arr[4]) != CarStatus.sold:
            s_date = None
            s_cost = None
        else:
            # Читаем индекс с продажами для определения строки в файле sales.txt
            with open(self._format_path('sales_index.txt'), 'r', encoding='utf-8') as si_file:
                si_file_lines: list[str] = si_file.readlines()
            
            sale_target_line = -1
            for line in si_file_lines:
                si_vin, line_number = line.rstrip().split(',')
                if si_vin == vin:
                    sale_target_line = int(line_number)
                    break
            if sale_target_line == -1:
                raise ValueError('Неправильный VIN')
            
            # Читаем  файл  с продажами
            with open(self._format_path('sales.txt'), 'r', encoding='utf-8') as sale_file:
                sale_file.seek(sale_target_line * 502)
                sale_line = sale_file.readline()
                sale_arr = sale_line.strip().split(',')
                print(sale_arr)
                s_date = datetime.strptime(sale_arr[2], "%Y-%m-%d %H:%M:%S")
                s_cost =Decimal(sale_arr[3])

        return CarFullInfo(
            vin= str(car_arr[0]),
            car_model_name= str(model_arr[1]),
            car_model_brand= str(model_arr[2]),
            price= Decimal(car_arr[2]),
            date_start= datetime.strptime(car_arr[3], "%Y-%m-%d %H:%M:%S"),
            status= CarStatus(car_arr[4]),
            sales_date= s_date,
            sales_cost= s_cost
        )

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
        raise NotImplementedError

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        raise NotImplementedError

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        raise NotImplementedError

    