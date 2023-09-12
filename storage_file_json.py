from abc import ABC, abstractmethod
from class_vacancy import Vacancy
import json


class FileStorage(ABC):

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancy(self, vacancy):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass


class JSONSaver(FileStorage):

    def __init__(self, filename):
        self.filename = filename.lower()

    def save_json(self, data):
        try:
            with open(self.filename, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Произошла ошибка при записи в файл: {e}")

    def load_vacancies(self):

        """ Функция чтения JSON файла. """

        try:
            with open(self.filename, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)

                vacansies_list = []
                for vacancy in data:
                    vacansies_list.append(Vacancy(**vacancy))

        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return None
        return vacansies_list

    def add_vacancy(self, vacancy):
        pass

    def get_vacancy(self, vacancy):
        pass

    def delete_vacancy(self, vacancy):
        pass

