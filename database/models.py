from database.db import get_conn
from datetime import datetime

def add_user(user_id, username):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO Users (user_id, username, registered_at) VALUES (?, ?, ?)", 
              (user_id, username, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_user(user_id):
    """Получить информацию о пользователе"""
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT user_id, username, email, balance, registered_at FROM Users WHERE user_id=?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def update_user_email(user_id, email):
    """Обновить email пользователя"""
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE Users SET email=? WHERE user_id=?", (email, user_id))
    conn.commit()
    conn.close()

def get_tours(page=1, per_page=3):
    """Получить туры с пагинацией"""
    conn = get_conn()
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM Tours WHERE status='active'")
    total = c.fetchone()[0]
    
    offset = (page - 1) * per_page
    
    c.execute("""
        SELECT tour_id, name, description, price, duration_days, status 
        FROM Tours WHERE status='active'
        ORDER BY tour_id
        LIMIT ? OFFSET ?
    """, (per_page, offset))
    tours = c.fetchall()
    conn.close()
    
    total_pages = (total + per_page - 1) // per_page if total > 0 else 1
    
    return tours, total_pages

def get_tour_by_id(tour_id):
    """Получить конкретный тур по ID"""
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT tour_id, name, description, price, duration_days, status FROM Tours WHERE tour_id=?", (tour_id,))
    tour = c.fetchone()
    conn.close()
    return tour

def add_favorite(user_id, tour_id):
    conn = get_conn()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO Favorites (user_id, tour_id, added_at) VALUES (?, ?, ?)",
                  (user_id, tour_id, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False

def remove_favorite(user_id, tour_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM Favorites WHERE user_id=? AND tour_id=?", (user_id, tour_id))
    conn.commit()
    conn.close()

def is_favorite(user_id, tour_id):
    """Проверить, в избранном ли тур"""
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id FROM Favorites WHERE user_id=? AND tour_id=?", (user_id, tour_id))
    result = c.fetchone() is not None
    conn.close()
    return result

def get_favorites(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute('''SELECT Tours.* FROM Favorites 
                 JOIN Tours ON Favorites.tour_id = Tours.tour_id 
                 WHERE Favorites.user_id=?''', (user_id,))
    favs = c.fetchall()
    conn.close()
    return favs

def add_progress(user_id, tour_id, amount):
    conn = get_conn()
    c = conn.cursor()
    
    c.execute('SELECT paid_amount FROM TourProgress WHERE user_id=? AND tour_id=?', (user_id, tour_id))
    existing = c.fetchone()
    
    if existing:
        c.execute('''
        UPDATE TourProgress SET paid_amount=paid_amount+?, updated_at=?
        WHERE user_id=? AND tour_id=?
        ''', (amount, datetime.now().isoformat(), user_id, tour_id))
    else:
        c.execute('''
        INSERT INTO TourProgress (user_id, tour_id, paid_amount, updated_at)
        VALUES (?, ?, ?, ?)
        ''', (user_id, tour_id, amount, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def get_progress(user_id, tour_id):
    """Получить накопленные средства для тура"""
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT paid_amount FROM TourProgress WHERE user_id=? AND tour_id=?', (user_id, tour_id))
    res = c.fetchone()
    conn.close()
    return res[0] if res else 0

def get_bookings(user_id):
    """Получить все бронирования пользователя"""
    conn = get_conn()
    c = conn.cursor()
    c.execute('''
        SELECT Bookings.booking_id, Tours.*, Bookings.status, Bookings.booked_at
        FROM Bookings
        JOIN Tours ON Bookings.tour_id = Tours.tour_id
        WHERE Bookings.user_id=?
        ORDER BY Bookings.booked_at DESC
    ''', (user_id,))
    bookings = c.fetchall()
    conn.close()
    return bookings

def make_booking(user_id, tour_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute('''
    INSERT INTO Bookings (user_id, tour_id, status, booked_at)
    VALUES (?, ?, ?, ?)
    ''', (user_id, tour_id, 'confirmed', datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_balance(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT balance FROM Users WHERE user_id=?', (user_id,))
    res = c.fetchone()
    conn.close()
    return res[0] if res else 0

def update_balance(user_id, amount):
    conn = get_conn()
    c = conn.cursor()
    c.execute('UPDATE Users SET balance=balance+? WHERE user_id=?', (amount, user_id))
    conn.commit()
    conn.close()
