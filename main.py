import sys
import locale

# Настройка кодировки для Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

import datetime
import time
from dataclasses import dataclass
from typing import List
import pickle
import random

@dataclass
class TravelPackage:
    package_id: str          # номер путевки (ключ)
    destination: str         # место назначения
    hotel_name: str         # название отеля
    start_date: datetime.date  # дата начала
    duration: int           # продолжительность в днях
    price: float           # стоимость

@dataclass
class IndexRecord:
    key: str  # ключ (номер путевки)
    position: int  # позиция в файле

class TravelDatabase:
    def __init__(self, filename: str):
        self.filename = filename
        self.index: List[IndexRecord] = []
    
    def add_package(self, package: TravelPackage):
        # Добавление путевки в файл
        with open(self.filename, 'ab') as f:
            position = f.tell()
            pickle.dump(package, f)
            # Добавление записи в индексный массив
            index_record = IndexRecord(package.package_id, position)
            self._insert_sorted(index_record)
    
    def _insert_sorted(self, record: IndexRecord):
        # Вставка с сохранением сортировки по ключу
        i = 0
        while i < len(self.index) and self.index[i].key < record.key:
            i += 1
        self.index.insert(i, record)
    
    def search_by_index(self, package_id: str) -> TravelPackage | None:
        # Бинарный поиск по индексному массиву
        left, right = 0, len(self.index) - 1
        
        while left <= right:
            mid = (left + right) // 2
            if self.index[mid].key == package_id:
                # Найден ключ - читаем данные из файла
                with open(self.filename, 'rb') as f:
                    f.seek(self.index[mid].position)
                    return pickle.load(f)
            elif self.index[mid].key < package_id:
                left = mid + 1
            else:
                right = mid - 1
        return None
    
    def search_sequential(self, package_id: str) -> TravelPackage | None:
        # Последовательный поиск в файле
        with open(self.filename, 'rb') as f:
            while True:
                try:
                    position = f.tell()
                    package = pickle.load(f)
                    if package.package_id == package_id:
                        return package
                except EOFError:
                    break
        return None

def generate_test_data(n: int) -> List[TravelPackage]:
    # Генерация тестовых данных
    destinations = ["Турция", "Египет", "Греция", "Испания", "Кипр", "Таиланд"]
    hotels = ["Sun Resort", "Beach Palace", "Grand Hotel", "Sea View", "Royal Resort"]
    packages = []
    
    for i in range(n):
        start_date = datetime.date(2024, random.randint(1, 12), random.randint(1, 28))
        package = TravelPackage(
            package_id=f"TUR{random.randint(10000, 99999)}",
            destination=random.choice(destinations),
            hotel_name=random.choice(hotels),
            start_date=start_date,
            duration=random.randint(7, 14),
            price=random.uniform(30000, 150000)
        )
        packages.append(package)
    return packages

def compare_search_methods(db: TravelDatabase, search_key: str, iterations: int = 100):
    # Сравнение времени поиска
    
    # Измерение времени индексного поиска
    start_time = time.time()
    for _ in range(iterations):
        db.search_by_index(search_key)
    index_time = time.time() - start_time
    
    # Измерение времени последовательного поиска
    start_time = time.time()
    for _ in range(iterations):
        db.search_sequential(search_key)
    sequential_time = time.time() - start_time
    
    print(f"\nComparison results ({iterations} iterations):")
    print(f"Index search time: {index_time:.4f} sec")
    print(f"Sequential search time: {sequential_time:.4f} sec")
    print(f"Index search is {sequential_time/index_time:.2f} times faster")

def main():
    db = TravelDatabase("travel_packages.dat")
    
    # Генерация тестовых данных
    test_size = 500  # Можно изменить размер для тестирования
    packages = generate_test_data(test_size)
    
    # Заполнение базы данных
    for package in packages:
        db.add_package(package)
    
    print(f"Database created. Number of records: {len(db.index)}")
    
    # Поиск путевки
    search_id = packages[random.randint(0, len(packages)-1)].package_id
    print(f"\nSearching for package ID: {search_id}")
    
    # Поиск через индексный массив
    package = db.search_by_index(search_id)
    if package:
        print(f"Found package: {package}")
        print(f"Destination: {package.destination}")
        print(f"Hotel: {package.hotel_name}")
        print(f"Start date: {package.start_date}")
        print(f"Duration: {package.duration} days")
        print(f"Price: {package.price:.2f} RUB")
    else:
        print("Package not found")
    
    # Сравнение методов поиска
    compare_search_methods(db, search_id)

if __name__ == "__main__":
    main()
