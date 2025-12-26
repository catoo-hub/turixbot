import sqlite3
import os
import json
from settings import DB_PATH

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    
    # == Users ==
    c.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        email TEXT,
        balance REAL DEFAULT 0,
        registered_at TEXT
    )
    ''')
    
    # == Tours ==
    c.execute('''
    CREATE TABLE IF NOT EXISTS Tours (
        tour_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        duration_days INTEGER,
        status TEXT DEFAULT 'active'
    )
    ''')
    
    # == Favorites ==
    c.execute('''
    CREATE TABLE IF NOT EXISTS Favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        tour_id INTEGER,
        added_at TEXT,
        UNIQUE(user_id, tour_id),
        FOREIGN KEY(user_id) REFERENCES Users(user_id),
        FOREIGN KEY(tour_id) REFERENCES Tours(tour_id)
    )
    ''')
    
    # == TourProgress ==
    c.execute('''
    CREATE TABLE IF NOT EXISTS TourProgress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        tour_id INTEGER,
        paid_amount REAL DEFAULT 0,
        updated_at TEXT,
        UNIQUE(user_id, tour_id),
        FOREIGN KEY(user_id) REFERENCES Users(user_id),
        FOREIGN KEY(tour_id) REFERENCES Tours(tour_id)
    )
    ''')
    
    # == Bookings ==
    c.execute('''
    CREATE TABLE IF NOT EXISTS Bookings (
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        tour_id INTEGER,
        status TEXT DEFAULT 'confirmed',
        booked_at TEXT,
        FOREIGN KEY(user_id) REFERENCES Users(user_id),
        FOREIGN KEY(tour_id) REFERENCES Tours(tour_id)
    )
    ''')
    
    conn.commit()
    
    # НЕЙРОСЕТЬ! == Загрузка туров из JSON при инициализации базы ==
    c.execute('SELECT COUNT(*) FROM Tours')
    count = c.fetchone()[0]
    
    print(f"[DEBUG] Туров в БД: {count}")
    
    if count == 0:
        if os.path.exists("data/tours.json"):
            with open("data/tours.json", "r", encoding="utf-8") as f:
                tours = json.load(f)
                for t in tours:
                    c.execute('''
                        INSERT INTO Tours (name, description, price, duration_days, status)
                        VALUES (?, ?, ?, ?, 'active')
                    ''', (t['name'], t['description'], t['price'], t['duration_days']))
                    print(f"[DEBUG] Добавлен тур: {t['name']} (id={c.lastrowid})")
                
                conn.commit()
                print(f"[OK] В базу добавлено туров: {len(tours)}")
        else:
            print("[WARN] Файл data/tours.json не найден")
    
    c.execute("SELECT tour_id, name FROM Tours")
    tours = c.fetchall()
    print(f"[DEBUG] Туры в БД после загрузки:")
    for t in tours:
        print(f"  - tour_id={t['tour_id']}, name={t['name']}")
    
    conn.close()
