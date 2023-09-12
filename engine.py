from abc import ABC, abstractmethod
import requests
from class_error import ParsingError

secret_key_sj = 'v3.r.137787279.119015fa0f76cb13db4a4c08899279b5de21641a.7437ad55167a84b2c7ecc31b34bfed415c19a7a6'


class VacancyAPI(ABC):

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def get_formatted_vacancies(self):
        pass


class HeadHunterAPI(VacancyAPI):

    def __init__(self, text, city):
        self.text = text
        self.city = city
        self.vacancies = []

    def get_city(self):
        while True:
            url = "https://api.hh.ru/areas/113"
            response = requests.get(url)
            data_file = response.json()
            found_city = False
            for item in data_file['areas']:
                if self.city in item['name']:
                    self.city = item['id']
                    found_city = True
                    break
            if found_city:
                break
            else:
                print("В этом городе нет вакансий. Пожалуйста, введите другой город.")
                self.city = input("Введите название города для поиска вакансии: ").title()

    def get_vacancies(self):
        url = 'https://api.hh.ru/vacancies'
        params = {
            'text': self.text,
            'area': self.city,
            'per_page': 50
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения вакансий! Статус: {response.status_code}")
        self.vacancies.append(response.json()['items'])
        return self.vacancies

    def get_formatted_vacancies(self):
        formatted_vacancies = []
        for vacancy in self.vacancies[0]:
            formatted_vacancy = {
                "title": vacancy["name"],
                "salary_from": vacancy["salary"]["from"] if vacancy["salary"] else None,
                "salary_to": vacancy["salary"]["to"] if vacancy["salary"] else None,
                "experience": vacancy["experience"]["name"],
                "city": vacancy["area"]["name"],
                "url": vacancy["url"]
            }
            formatted_vacancies.append(formatted_vacancy)
        return formatted_vacancies


class SuperJobAPI(VacancyAPI):

    def __init__(self, text, city):
        self.text = text
        self.city = city
        self.vacancies = []

    def get_city(self):
        while True:
            url = "https://api.superjob.ru/2.0/towns/"
            response = requests.get(url)
            data_file = response.json()
            found_city = False
            if 'objects' in data_file:
                for item in data_file['objects']:
                    if self.city in item['title']:
                        self.city = item['id']
                        found_city = True
                        break
                if found_city:
                    break
                else:
                    print("В этом городе нет вакансий. Пожалуйста, введите другой город.")
                    self.city = input("Введите название города для поиска вакансии: ").title()

    def get_vacancies(self):
        url = 'https://api.superjob.ru/2.0/vacancies'

        headers = {
            "X-Api-App-Id": secret_key_sj
        }
        params = {
            'keyword': self.text,
            'towns': self.city,
            'count': 50
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения вакансий! Статус: {response.status_code}")
        self.vacancies.append(response.json()['objects'])
        return self.vacancies

    def get_formatted_vacancies(self):
        formatted_vacancies = []
        for vacancy in self.vacancies[0]:
            formatted_vacancy = {
                "title": vacancy["profession"],
                "salary_from": vacancy["payment_from"] if vacancy["payment_from"] else None,
                "salary_to": vacancy["payment_to"] if vacancy["payment_to"] else None,
                "experience": vacancy["experience"]["title"],
                "city": vacancy["town"]["title"],
                "url": vacancy["link"]
            }
            formatted_vacancies.append(formatted_vacancy)
        return formatted_vacancies
