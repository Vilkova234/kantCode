import json

def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['results']['vacancies']

def validate_vacancies(vacancies):
    errors_found = 0
    
    print("=== ЗАПУСК ВАЛИДАЦИИ ВАКАНСИЙ ===\n")
    
    for item in vacancies:
        vacancy = item['vacancy']
        v_id = vacancy['id']
        job_name = vacancy['job-name'] # <-- ИСПРАВЛЕНО: убрана буква r
        
        vac_errors = []
        
        # 1. Проверка зарплаты (ловушка: max = 0 или min = 0)
        salary_min = vacancy.get('salary_min', 0)
        salary_max = vacancy.get('salary_max', 0)
        
        if salary_min == 0 or salary_max == 0:
            vac_errors.append(f"Ошибка зарплаты: Указана нулевая зарплата (min: {salary_min}, max: {salary_max}).")
        elif salary_min > salary_max:
            vac_errors.append(f"Ошибка зарплаты: Минимальная зарплата ({salary_min}) больше максимальной ({salary_max}).")

        # Получаем текст для анализа
        qualification = vacancy.get('requirement', {}).get('qualification', '').lower()
        experience = vacancy.get('requirement', {}).get('experience', 0)
        duty = vacancy.get('duty', '').lower()
        schedule = vacancy.get('schedule', '').lower()

        # 2. Проверка опыта (ловушка: в поле 0 лет, а в тексте требуется 5 лет)
        if experience == 0 and ("лет опыта" in qualification or "года опыта" in qualification):
            vac_errors.append("Ошибка опыта: В поле experience указан 0, но в квалификации требуется опыт работы.")

        # 3. Проверка удаленной работы (ловушка: в обязанностях "дистанционная", а в требованиях "присутствие в офисе")
        if "дистанционн" in duty and ("офис" in qualification or "присутствие" in qualification):
            vac_errors.append("Ошибка формата работы: В обязанностях указана дистанционная работа, но в требованиях — обязательное присутствие в офисе.")

        # 4. Проверка графика (ловушка: "гибкий график", но в тексте строгие часы)
        if "гибкий" in schedule and ("09:00" in qualification or "18:00" in qualification):
            vac_errors.append("Ошибка графика: Указан гибкий график, но в требованиях прописаны строгие рабочие часы.")

        # 5. Проверка размытых требований (ловушка: "Не указано" образование)
        education = vacancy.get('requirement', {}).get('education', '')
        if education == "Не указано":
            vac_errors.append("Предупреждение: Не указано требуемое образование.")

        # Вывод результатов по вакансии
        if vac_errors:
            print(f"[!] Найдены проблемы в вакансии {v_id} ({job_name}):")
            for err in vac_errors:
                print(f"    - {err}")
            print("-" * 50)
            errors_found += len(vac_errors)

    print(f"\n=== ИТОГО НАЙДЕНО ОШИБОК: {errors_found} ===")

if __name__ == "__main__":
    # ВАЖНО: Убедитесь, что здесь написано ТОЧНОЕ имя вашего JSON-файла (с учетом регистра и расширения)
    # Если ваш файл называется manege.json, напишите 'manege.json'. Если validator.json - напишите 'validator.json'
    filename = 'manege.json' 
    
    try:
        data = load_data(filename)
        validate_vacancies(data)
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден в папке с программой.")