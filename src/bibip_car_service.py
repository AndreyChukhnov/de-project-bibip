from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
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

"""_summary_
"""
class CarService:
    # внутри класса инициируем метод для формирования пути для сохранения файлов
    def _format_path(self, filename: str) -> str:
        return os.path.join(self.root_directory_path, filename)
    
    # внутри класса инициирцем метод для чтения файла исформированного в методе _format_path
    # который формирует файл список списка строк при условии отсутвия файла в указанной директории 
    def _read_file(self, filename: str) -> list[list[str]]:
        if not os.path.exists(self._format_path(filename)):
            return []
        else:
            with open(self._format_path(filename), 'r') as f:
                lines = f.readlines()
                split_lines = [l.strip().split(',') for l in lines]
                return split_lines
            
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path
        self.model_index: list[ModelIndex] = []
        self.car_index: list[CarIndex] = []

        split_model_lines = self._read_file("models_index.txt")
        self.model_index = [ModelIndex(int(l[0]), int(l[1])) for l in split_model_lines]

        split_car_lines = self._read_file('cars_index.txt')
        self.car_index = [CarIndex(int(l[0]), int(l[1])) for l in split_car_lines]

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        # открываем файл  models на добавление строк и формируем строки из атрибутов класса Model
        with open(self._format_path('models.txt'), 'a') as f:
            str_model = f'{model.id}, {model.name}, {model.brand}'.ljust(500) + '\n'
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

        new_ci = CarIndex(car.vin, len(self.model_index))

        self.car_index.append(new_ci)
        self.car_index.sort(key=lambda x: x.car_id)

        with open(self._format_path("cars_index.txt"), "w") as f:
            for current_mi in self.car_index:
                str_car = f"{current_mi.car_id},{current_mi.position_in_file_cars}".ljust(50)
                f.write(str_car + "\n")

        return car

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        raise NotImplementedError

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        raise NotImplementedError

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
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
