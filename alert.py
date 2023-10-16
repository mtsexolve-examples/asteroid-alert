import requests
from datetime import date

# Сегодняшняя дата
todays_date = date.today().strftime("%Y-%m-%d")

# Настройки подключения к NASA API: ключ и URL
# NASA API-ключ можно получиь здесь: https://api.nasa.gov/

nasa_api_key = "NASA_API_KEY"
nasa_url = "https://api.nasa.gov/neo/rest/v1/feed?start_date=" + todays_date +"&end_date="+ todays_date + "&api_key="+nasa_api_key

# Отправляем запрос в NASA API и получаем ответ в JSON
nasa_response = requests.get(nasa_url)
json_nasa_response = nasa_response.json()

# Функция для нахождения индекса ближайшего к Земле астеройда в массиве всех близких астеройдов
def find_closest_asteroid_index(near_asteroids):
    # пустой массив для учёта дальности астероидов от Земли
    asteroids = []
    # перебираем астероиды в массиве near_earth_objects
    for i in range(0, len(near_asteroids)):
        # добавляем расстоядобавляем расние до Земли в массив
        asteroids.insert(i, near_asteroids[i]['close_approach_data'][0]['miss_distance']['kilometers'])
    # находим минимальное расстояние в массиве и возвращаем его индекс
    # индекс будет совпадать с индексом ближайшего астероида в near_earth_objects    
    return asteroids.index(min(asteroids))

# Если около Земли есть астероиды
if "near_earth_objects" in json_nasa_response:
    # Получаем список близких астероидов
    near_asteroids = json_nasa_response['near_earth_objects'][todays_date]
    # Индекс ближайшего астероида
    closest_asteroid_index = find_closest_asteroid_index(near_asteroids)

    # Получаем данные астероида, которые отправим в SMS-уведомлении
    name = near_asteroids[closest_asteroid_index]['name'] #название астероида
    how_close = near_asteroids[closest_asteroid_index]['close_approach_data'][0]['miss_distance']['kilometers'] #расстояние от Земли
    diameter =  near_asteroids[closest_asteroid_index]['estimated_diameter']['meters']['estimated_diameter_max'] #диаметр астероида

    # Форматируем данные в строку
    how_close_str = str(round(float(how_close)))
    diameter_str = str(round(diameter))
    
    # Формируем сообщение
    alert ="Ближайший астеройд сегодня - " + name + ". Он находится в " + how_close_str + " км от Земли. Его диаметр составляет " + diameter_str + " метров."


    # Настройки подключения к Exolve
    exolve_number = "7999XXXXXXX"
    exolve_url = "https://api.exolve.ru/messaging/v1/SendSMS"
    recipient_number = "7924XXXXXXX"
    exolve_api_key = "EXOLVE_API_KEY"

    # Отправляем запрос в EXOVE SMS API и получаем ответ в JSON
    exolve_response = requests.post(exolve_url, 
    headers = {"Authorization": "Bearer " + exolve_api_key},
    json = {
        "number": exolve_number,
        "destination": recipient_number,
        "text": alert
    })
    json_exolve_response = exolve_response.json()
    print(json_exolve_response) # message_id или ошибка отправки



