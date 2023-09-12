class Vacancy:

    def __init__(self, title, salary_from, salary_to, experience, city, url):
        self._title = title
        self._salary_from = salary_from
        self._salary_to = salary_to
        self._experience = experience
        self._city = city
        self._url = url

    def __str__(self):
        return f"""Вакансия: {self._title}
Зарплата: {self._salary_from} до {self._salary_to} руб.
Опыт: {self._experience}
Город: {self._city}
Ссылка на вакансию: {self._url}"""

    def __lt__(self, other):
        if self._salary_from and other.salary_from is not None:
            return self._salary_from < other.salary_from

    @property
    def salary_from(self):
        return self._salary_from