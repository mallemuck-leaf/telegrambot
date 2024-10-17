import sqlite3


def create_tables():
    # создание бд для работы памяти
    with sqlite3.connect('points.db') as conn:
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cities (
                id INTEGER PRIMARY KEY,
                city VARCHAR,
                lat VARCHAR,
                lon VARCHAR
            )
            ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                chat_id INTEGER PRIMARY KEY,
                last_city INTEGER REFERENCES cities(id)
            )
            ''')


def get_city(city):
    # поиск сохраненнных координат городов
    with sqlite3.connect('points.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM cities WHERE city = ?
        ''', (city,))
    return cursor.fetchone()


def get_city_id(id):
    # поиск сохраненнных координат городов
    with sqlite3.connect('points.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM cities WHERE id = ?
        ''', (id,))
    return cursor.fetchone()


def add_city(city, lat, lon):
    # добавление координат в базу чтобы не опрашивать сервера
    with sqlite3.connect('points.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO cities (city, lat, lon) VALUES (?, ?, ?)
        ''', (city, lat, lon))


def add_info(chat_id, city):
    # сохранение последнего города для чата
    with sqlite3.connect('points.db') as conn:
        cursor = conn.cursor()
        # print(get_city(city))
        new_city = get_city(city)
        if new_city is not None:
            city_id = get_city(city)[0]
        cursor.execute('''
        SELECT * FROM sessions WHERE chat_id = ?
        ''', (chat_id,))
        chat_id_db = cursor.fetchone()
        print(chat_id_db)
        if chat_id_db is not None:
            cursor.execute(f'''
            UPDATE sessions 
            SET last_city = {city_id}
            WHERE chat_id = {chat_id}
            ''')
        else:
            cursor.execute('''
            INSERT INTO sessions (chat_id, last_city) VALUES (?, ?)
            ''', (chat_id, city_id))


def get_info(chat_id):
    # поиск последних сохраненных данных для чата
    with sqlite3.connect('points.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM sessions WHERE chat_id = ?
        ''', (chat_id,))
        return cursor.fetchone()


if __name__ == '__main__':
    print('bot_data.py')
    create_tables()
    print(get_city('Минск'))
    # add_city('Minsk', 138, 758)
    # print(get_city('Minsk'))
    print(get_info(17812385))
    add_info(17812385, 'Minsk')
    print(get_info(17812385))
