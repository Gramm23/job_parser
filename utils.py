from engine import HeadHunterAPI, SuperJobAPI
from storage_file_json import JSONSaver

selected_number = None


def save_vacancies_to_file(number):
    global selected_number
    while True:
        print()
        answer_vacancy = str(input("Введите поисковый запрос вакансии: "))
        city_selection = str(input("Введите название города для поиска вакансии: ").title())
        hh = HeadHunterAPI(answer_vacancy, city_selection) if number in (1, 3) else None

        sj = SuperJobAPI(answer_vacancy, city_selection) if number in (2, 3) else None

        vacancies_to_save = []

        if hh:
            hh.get_city()
            hh.get_vacancies()
            vacancies_hh = hh.get_formatted_vacancies()
            vacancies_to_save.extend(vacancies_hh)

        if sj:
            sj.get_vacancies()
            vacancies_sj = sj.get_formatted_vacancies()
            vacancies_to_save.extend(vacancies_sj)

        saver_file = JSONSaver("vacancy_file.json")
        saver_file.save_json(vacancies_to_save)

        selected_number = number
        break
    return selected_number


def display_vacancy_options(number):
    global selected_number
    while True:
        if number in (1, 2, 3, 4) and selected_number in (1, 2, 3):
            saver_file = JSONSaver("vacancy_file.json")
            result = saver_file.load_vacancies()

            if result is not None:
                if number == 1:
                    print("Показать все вакансии:")
                    help_func(result)
                    break
                elif number == 2:
                    print("Показать вакансии по зарплате (по убыванию):")
                    result.sort(key=lambda x: x.salary_from if x.salary_from is not None else 0, reverse=True)
                    help_func(result)
                    break
                elif number == 3:
                    print("Показать вакансии по зарплате (по возрастанию):")
                    result.sort(key=lambda x: x.salary_from if x.salary_from is not None else 0, reverse=False)
                    help_func(result)
                    break
                elif number == 4:
                    top_n = int(input("Введите количество вакансий для отображения: "))
                    print(f"Показать топ {top_n} вакансий:")
                    selected_number = number  # Обновляем значение selected_number
                    result.sort(key=lambda x: x.salary_from if x.salary_from is not None else 0, reverse=True)
                    help_func(result[:top_n])
                    break
                break


def help_func(data):
    for vacancy in data:
        print()
        print(vacancy)
