import matplotlib.pyplot as plt
import numpy as np
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

'''
 Задача №1. Создай гистограмму для случайных данных,
 сгенерированных с помощью функции `numpy.random.normal`.
'''
# Параметры нормального распределения
mean = 0 # Среднее значение
std_dev = 1 # Стандартное отклонение
num_samples = 1000 # Количество образцов

# Генерация случайных чисел, распределенных по нормальному распределению
data = np.random.normal(mean, std_dev, num_samples)

# Генерация гистограммы
plt.hist(data, bins=30)
plt.show()

'''
 Задача №2. Построй диаграмму рассеяния для двух наборов случайных данных,
 сгенерированных с помощью функции `numpy.random.rand`.
'''
# Генерация случайных чисел
random_array1 = np.random.rand(500) # массив из 500 случайных чисел
random_array2 = np.random.rand(500) # массив из 500 случайных чисел

# Генерация диаграммы рассеяния
plt.scatter(random_array1, random_array2)
plt.show()

'''
 Задача №3. Необходимо спарсить цены на диваны с сайта divan.ru в csv файл,
 обработать данные, найти среднюю цену и вывести ее,
 а также сделать гистограмму цен на диваны.
'''
# Функция для парсинга страницы
def parse_page(driver, url):
    driver.get(url)  # Открываем веб-страницу
    try:
        # Ждем, пока элемент с классом 'CE4Nr' станет доступен
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.catalog-product")))
    except Exception as e:
        print(f"Не удалось загрузить страницу: {e}")
        return []

    # Находим все карточки товаров
    divans = driver.find_elements(By.CSS_SELECTOR, "div.CE4Nr")

    page_data = []
    # Перебираем коллекцию товаров
    for good in divans:
        try:
            name = good.find_element(By.CSS_SELECTOR, 'a[tabindex="0"] span[itemprop="name"]').text
            price = good.find_element(By.CSS_SELECTOR, 'meta[itemprop="price"]').get_attribute("content")
            page_data.append([name, price])
        except Exception as e:
            print(f"Не удалось получить данные товара: {e}")

    return page_data

divanes_data = []  # Создаём список, в который потом всё будет сохраняться
driver = webdriver.Chrome()

# Парсим страницы с 1 по 9 (или больше, если нужно)
for page_num in range(1, 10):
    url = f"https://www.divan.ru/category/pramye-divany/page-{page_num}"
    print(f"Парсинг страницы: {url}")
    divanes_data.extend(parse_page(driver, url))
    time.sleep(2)  # Небольшая пауза между запросами

# Закрываем подключение браузер
driver.quit()

# Прописываем открытие нового файла, задаём ему название и форматирование
with open(f"price_divanes9.csv", 'w',newline='', encoding='utf-8') as file:
    # Используем модуль csv и настраиваем запись данных в виде таблицы
    writer = csv.writer(file)
    # Создаём заголовок таблицы
    # writer.writerow(['Название товара', 'Цена'])
    # Прописываем использование списка как источник для записи таблицы
    writer.writerows(divanes_data)
print('done')

# Чтение CSV файла и создание DataFrame из данных
df = pd.DataFrame(pd.read_csv('price_divanes1.csv'))
# Преобразуем колонку "Цена" к числовому типу,
# удаляя символы валюты и другие нечисловые символы
mean_price = df['Цена'].mean()
mean_price = "Средняя цена = " + "{:.2f}".format(mean_price) + " руб."
# Вывод результатов
print(mean_price)

df = df.dropna(subset=['Цена'])

# Строим гистограмму
plt.figure(figsize=(10, 6))
plt.hist(df['Цена'], bins=10, edgecolor='black')

# Добавляем заголовок и метки осей
plt.title(f'Гистограмма цен диванов на сайте www.divan.ru\n {mean_price}')
plt.xlabel('Цена (руб)')
plt.ylabel('Количество диванов')

# Показываем гистограмму
plt.show()
