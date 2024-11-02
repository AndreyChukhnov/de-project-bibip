from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
from decimal import Decimal
from datetime import datetime
import os
from collections import Counter

# Инициируем класс индексов для таблицы models
class ModelIndex:
     """Класс индеков models"""
     def __init__(self, model_id: int, position_in_file_models: int):
        self.model_id = model_id
        self.position_in_file_models = position_in_file_models

# Инициируем класс индексов для таблицы cars
class CarIndex:
    """Класс индексов cars"""
    def __init__(self, car_id: str, position_in_file_cars: int):
        self.car_id = car_id
        self.position_in_file_cars = position_in_file_cars

# Инимциируем клас нидексов для таблицы sales
class SaleIndex:
    """Класс индексов sales"""
    def __init__(self, sale_id:str, position_in_file_sales: int):
        self.sale_id = sale_id
        self.position_in_file_sales = position_in_file_sales


class CarService:
    """ 
    Класс CarService реализует различные методы для для работы с данными
    автосалона БиБип. Среди них:
    - сохранение моделей и формирования индекса по ключевому полю
    - сохранение автомобилей и формирование индекса по ключевому полю
    - сохранение сохранение продаж и формирование индекса по vin, а так же
        внесение изменнеия статуса авто после продажи
    - получение списка списка доступных к продаже аавтомобилей 
    - получение детальной информации об автомобилей
    - обновление ключевого поля
    - удаление строки в sales
    - формирование списка трех самых продаваемых моделей 
        с их колчеством 
    """
    def _format_path(self, filename: str) -> str:
        """ Приватный метод
            Объединяет root_directory_path и имя файла для получения полного пути
        """
        return os.path.join(self.root_directory_path, filename)
    
    def _read_file(self, filename: str) -> list[list[str]]:
        """ Приватный метод
            Читает файл и формирует список списков строк
        """
        if not os.path.exists(self._format_path(filename)):
            return []
        else:
            with open(self._format_path(filename), 'r', encoding='utf-8') as f:
                lines = f.readlines()
                split_lines = [l.strip().split(',') for l in lines]
                return split_lines
            
    def _get_model_info(self, model_id: str) -> Model:
        """ Приватный метод  для получения информации о модели по id """
        # читаем индекс и определяем номер строки в models
        with open(self._format_path('models_index.txt'), 'r', encoding='utf-8') as mi_file:
            for line in mi_file:
                mod_id, line_number = line.strip().split(',')
                if mod_id == model_id:
                    target_string = int(line_number) # искомая строка в models
                    break
            else:
                raise ValueError('Модели с таким id нет в sales')
        # в models читаем нужную нам строку и формируем из нее массив
        with open(self._format_path('models.txt'), 'r', encoding='utf-8') as model_file:
            model_file.seek(target_string * 502)
            model_arr = model_file.readline().strip().split(',')

        # возврашаем экземрляр класса Model c нужными атрибутами
        return Model(id=model_arr[0], name=model_arr[1], brand=model_arr[2])    
            
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
        """ Метод для добавления новых строк в models и обновления индекса"""
        # открываем файл  models на добавление строк и формируем строки из атрибутов класса Model
        with open(self._format_path('models.txt'), 'a') as f:
            str_model = f'{model.id},{model.name},{model.brand}'.ljust(500) + '\n'
            f.write(str_model)
        
        # Создаем экемпляр сласса ModelIndex
        new_mi = ModelIndex(model.id, len(self.model_index))
        # Добавляем new_mi в атрибут model_index
        self.model_index.append(new_mi)
        # сортируем атрибут по ключевому полю
        self.model_index.sort(key=lambda x: x.model_id)

        # перезаписываем индекс в сответвсии с обновленным атрибутом model_index
        with open(self._format_path("models_index.txt"), "w") as f:
            for current_mi in self.model_index:
                str_model = f"{current_mi.model_id},{current_mi.position_in_file_models}".ljust(50)
                f.write(str_model + "\n")
        
        return model

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        """ Метод для добавления новых строк в cars и обновления индекса"""
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
        """ Метод для сохранения продажи,
            а так же для изменения статуса автомобиля в cars
        """
        # добавление строки в sales
        with open(self._format_path('sales.txt'), 'a', encoding='utf-8') as sales_file:
            sales_string = f'{sale.sales_number},{sale.car_vin},{sale.sales_date},{sale.cost}'.ljust(500)
            sales_file.write(sales_string + '\n')
        # добавление элемента в атрибут и его сортировка
        new_si = SaleIndex(sale_id=sale.car_vin, position_in_file_sales=len(self.sale_index))

        self.sale_index.append(new_si)
        self.sale_index.sort(key=lambda x: x.sale_id)
        # Перезапись индекса cars
        with open(self._format_path('sales_index.txt'), 'w', encoding='utf-8') as index_file:
           for element in self.sale_index:
               string = f'{element.sale_id},{element.position_in_file_sales}'.ljust(50)
               index_file.write(string + '\n')
        
        # читаем индекса cars и поиск номера строки по vin из продажи
        with open(self._format_path('cars_index.txt'), 'r', encoding='utf-8') as index_file:
            ci_string: list[str] = index_file.readlines()
            target_string = -1
            for element in ci_string:
                vin, line_number = element.strip().split(',')
                if vin.strip() == sale.car_vin:
                    target_string = int(line_number)
                    break
            if target_string == -1:
                raise ValueError('Машина не найдена')
        # чтение и перезапись строки с измененным статусом 
        # открываем cars для чтения и записи на определенной строке
        with open(self._format_path('cars.txt'), 'r+', encoding='utf-8') as car_file:
            car_file.seek(target_string * 502)
            car_line = car_file.readline()
            car_arr = car_line.strip().split(',')
            # Формируем экземляр класса Car
            car = Car(
                vin=str(car_arr[0]), 
                model=int(car_arr[1]), 
                price = Decimal(car_arr[2]), 
                date_start = datetime.strptime(car_arr[3], "%Y-%m-%d %H:%M:%S"), 
                status=CarStatus(car_arr[4])
                )
            # Изменяем значение атрибута на Sold
            car.status = CarStatus.sold
            # переписываем строку
            car_file.seek(target_string * 502)
            correct_line = f'{car.vin},{car.model},{car.price},{car.date_start},{car.status}'.ljust(500)
            car_file.write(correct_line + '\n')
            
        return car

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        """ Метод для определиния списка доступных к продаже машин """
        # Открываем cars на чтение
        with open(self._format_path('cars.txt'), 'r') as car_file:
            car_lines: list[str] = car_file.readlines()
            # формируем список строк
            car_line_split = [line.strip().split(',') for line in car_lines]
            # Для каждой строки создаем объект класса Car и добавляем его в список
            # при условии наличия у авто статуса "available"
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
        # Определяем номер строки по vin
        target_line = -1
        for line in lines:
            car_id, line_number = line.strip().split(',')
            if car_id == vin:
                target_line = int(line_number)
                break
        if target_line == -1:
            return None

        # Читаем строку в файле cars и формируем массив 
        with open(self._format_path('cars.txt'), 'r', encoding='utf-8') as car_file:
            car_file.seek(target_line * 502)
            car_line = car_file.readline()
            car_arr = car_line.strip().split(',')
        # Определяем id модели для получения инфо из models
        model_id = int(car_arr[1])

        # Читаем индекс для определения номера строки models по model_id
        with open(self._format_path('models_index.txt'), 'r', encoding='utf-8') as mi_file:
            mi_file_lines: list[str] = mi_file.readlines()

        # определяем номер строки в файле models
        model_target_line = -1
        for line in mi_file_lines:
            m_id, line_number = line.strip().split(',')
            if model_id == int(m_id):
                model_target_line = int(line_number)
                break
        if model_target_line == -1:
            raise ValueError('Неправильный VIN')
        
        # Читаем файлt models по номеру строки и формируем масив 
        with open(self._format_path('models.txt'), 'r', encoding='utf-8') as model_file:
            model_file.seek(model_target_line * 502)
            model_line = model_file.readline()
            model_arr = model_line.strip().split(',')

        # если машина не продана вернем none для даты продаж и суммы продажи
        if  str(car_arr[4]) != CarStatus.sold:
            s_date = None
            s_cost = None

        else:
            # Читаем индекс с продажами для определения строки в файле по vin
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
                s_date = datetime.strptime(sale_arr[2], "%Y-%m-%d %H:%M:%S")
                s_cost =Decimal(sale_arr[3])

        # Возвращаем объект класса CarFullInfo с атрибутами собранными 
        # полученных нами массивов
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
        # читаем индекс cars и проверяем существует ли запись в индексе
        with open(self._format_path('cars_index.txt'), 'r', encoding='utf-8') as index_file:
            index_lines = index_file.readlines()
        target_line = -1
        for line in index_lines:
            car_id, line_number = line.strip().split(',')
            if car_id == vin:
                target_line = int(line_number)
                break
        if target_line == -1:
            raise ValueError("Автомобиль с указанным VIN не найден.")
        print(target_line)

        # Читаем данные об автомобиле с возможность перезаписи
        with open(self._format_path('cars.txt'), 'r+', encoding='utf-8') as car_file:
            car_file.seek(target_line * 502)
            car_line = car_file.readline()
            car_arr = car_line.strip().split(',')
            print(car_arr)
            # Обновляем VIN в массиве
            car_arr[0] = new_vin
            print(car_arr[0])

            # перезаписываем строку в cars
            car_file.seek(target_line * 502)
            new_line = ','.join(car_arr).ljust(500)
            car_file.write(new_line + '\n')
        
        # обновляем индекс cars в атрибуте класса CarService
        for index in self.car_index:
            if index.car_id == vin:
                index.car_id = new_vin

        # Сортируем атрибу car_index класса CarServiceиндекс по car_id
        self.car_index.sort(key=lambda x: x.car_id)

        # Перезаписываем индекс cars
        with open(self._format_path("cars_index.txt"), "w") as f:
            for current_mi in self.car_index:
                str_car = f"{current_mi.car_id},{current_mi.position_in_file_cars}".ljust(50)
                f.write(str_car + "\n")

        car = Car(
            vin=new_vin,
            model=int(car_arr[1]),
            price=Decimal(car_arr[2]),
            date_start=datetime.strptime(car_arr[3], "%Y-%m-%d %H:%M:%S"),
            status=CarStatus(car_arr[4])
            )

        return car

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        # 1. Читаем файл продаж, чтобы найти vin и номер строки на удаление
        target_line = -1  # номер строки для удаления
        vin = None

        with open(self._format_path('sales.txt'), 'r', encoding='utf-8') as sales_file:
            sale_lines = sales_file.readlines()  # Читаем строки сразу
            for line_number, line in enumerate(sale_lines):
                sales_num, car_vin, _, _ = line.strip().split(',')
                if sales_num == sales_number:
                    vin = car_vin
                    target_line = line_number  # Сохраняем номер строки
                    break

        if target_line == -1:
            raise ValueError('Продажа не найдена')
        else:
            print(f"Удаляемая строка: {sale_lines[target_line].strip()} на позиции {target_line}")

        # 2 обновляем статус автомобиля
        # читаем индекс для поиска номера строки в cars
        with open(self._format_path('cars_index.txt'), 'r', encoding='utf-8') as index_file:
            index_lines = index_file.readlines()
        ci_line = -1
        for line in index_lines:
            car_id, line_number = line.strip().split(',')
            if car_id == vin:
                ci_line = int(line_number)
                break
        if ci_line == -1:
            raise ValueError(f'Машина с VIN {vin} не найдена')
        
        # Обновляем статус, для этого создадим объект car с атрибутами по найденной по найденной строке 
        with open(self._format_path('cars.txt'), 'r+', encoding='utf-8') as car_file:
            car_file.seek(ci_line * 502)
            car_line = car_file.readline()
            car_arr = car_line.strip().split(',')

            car = Car(
                vin=str(car_arr[0]),
                model=int(car_arr[1]),
                price=Decimal(car_arr[2]),
                date_start=datetime.strptime(car_arr[3], "%Y-%m-%d %H:%M:%S"),
                status=CarStatus(car_arr[4])
            )
            # обновляем статус
            car.status = CarStatus.available
            # Перезаписываем строку в файле cars
            correct_line = f'{car.vin},{car.model},{car.price},{car.date_start},{car.status}'.ljust(500)
            car_file.seek(ci_line * 502)
            car_file.write(correct_line + '\n')

        # Удаляем запись из sales.txt
        with open(self._format_path('sales.txt'), 'w', encoding='utf-8') as sales_file:
            for line_number, line in enumerate(sale_lines):
                if line_number != target_line:  # Пропускаем строку с удаляемой продажей
                    sales_file.write(line)
        
        # переписываем индекс продаж
        with open(self._format_path('sales.txt'), 'r', encoding='utf-8') as sales_file:
            sale_lines = sales_file.readlines()

        sales_index = []
        for line_number, line in enumerate(sale_lines):
            _, car_vin, _, _ = line.strip().split(',')
            sales_index.append((car_vin, line_number))

        # Сортируем по VIN
        sales_index.sort(key=lambda x: x[0])

        # обновляем индекс
        with open(self._format_path('sales_index.txt'), 'w', encoding='utf-8') as index_file:
            for car_vin, line_number in sales_index:
                index_file.write(f'{car_vin},{line_number}'.ljust(50) +'\n')

        
        return car         

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        # читаем sales и форммируем список vin
        with open(self._format_path('sales_index.txt'), 'r', encoding='utf-8') as si_file:
            sales_lines:list[str] = si_file.readlines()
        car_vin_list = []
        for s_line in sales_lines:
            car_vin, _ = s_line.strip().split(',')
            car_vin_list.append(car_vin)
        # последовательно читаем индекс cars по списку vin для определения номера строки
        # последовательно по номеру строки в индексе формируем список id
        model_id_list = []
        for element in car_vin_list:
            with open(self._format_path('cars_index.txt'), 'r', encoding='utf-8') as index_file:
                index_lines: list[str] = index_file.readlines()
                target_string = -1
                for ci_line in index_lines:
                    car_vin, line_number = ci_line.strip().split(',')
                    if car_vin == element:
                        target_string = int(line_number)
                        break
            with open(self._format_path('cars.txt'), 'r+', encoding='utf-8') as car_file:
                car_file.seek(target_string * 502)
                car_line = car_file.readline()
                car_arr = car_line.strip().split(',')
                model_id_list.append(car_arr[1])
        
        # формируем словарь с количеством продаж по id
        top_models = dict(Counter(model_id_list))
        #сортируем словарь по количеству продаж и оставляем срез из первых 3 
        top_3_models = sorted(top_models.items(), key=lambda x: x[1], reverse=True)[:3]        

        # Формируем список экземпляров ModelSaleStats для каждого элемента словаря
        result = []
        for model_id, sales_number in top_3_models:
            model_info = self._get_model_info(model_id)
            result.append(ModelSaleStats(car_model_name=str(model_info.name),
                                        brand=model_info.brand,
                                        sales_number=sales_number))

        return result
  