import os
from os.path import join, dirname
from dotenv import load_dotenv
import sqlite3

env_path = join(dirname(__file__), '.env')
db_path = join(dirname(__file__), 'database/source.db')


# ==Загрзука секретов из файла==
load_dotenv(env_path)

TOKEN = os.environ.get("TOKEN")


# ==Инциализация базы данных==
def intilizateDb():
    db = sqlite3.connect(db_path)
    cur = db.cursor()

    # ==Пользователи==
    cur.execute("""CREATE TABLE Users (
        user_id BIGINT PRIMARY KEY,
        username VARCHAR(100),
        email VARCHAR(255),
        balance DECIMAL(10,2) DEFAULT 0.00,
        registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # ==Избранное==
    cur.execute("""CREATE TABLE Favorites (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        tour_id INT NOT NULL,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (tour_id) REFERENCES Tours(tour_id) ON DELETE CASCADE,
        UNIQUE (user_id, tour_id)
    );
    """)

    # ==Туры==
    cur.execute("""CREATE TABLE Tours (
        tour_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        price DECIMAL(10,2) NOT NULL,
        duration_days INT,
        status VARCHAR(20) DEFAULT 'active'  -- active, booked, cancelled
    );
    """)

    # ==Прогресс по туру==
    cur.execute("""CREATE TABLE TourProgress (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        tour_id INT NOT NULL,
        paid_amount DECIMAL(10,2) DEFAULT 0.00,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (tour_id) REFERENCES Tours(tour_id) ON DELETE CASCADE,
        UNIQUE (user_id, tour_id)
    );
    """)

    # ==Буккинг==
    cur.execute("""CREATE TABLE Bookings (
        booking_id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        tour_id INT NOT NULL,
        status VARCHAR(20) DEFAULT 'pending',  -- pending, confirmed, cancelled
        booked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (tour_id) REFERENCES Tours(tour_id) ON DELETE CASCADE
    );
    """)

    db.commit()
    cur.close()
    db.close()