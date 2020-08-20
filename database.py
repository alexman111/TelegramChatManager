import sqlite3
import time


def add(user_id, date, username):
    conn = sqlite3.connect('server.db')
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO users VALUES(?, ?, ?)""", (user_id, date, username))
    conn.commit()


def remove(date):
    conn = sqlite3.connect('server.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE premium_date<?", (date,))
    conn.commit()


def remove_by_id(id):
    conn = sqlite3.connect('server.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE user_id=?", (id,))
    conn.commit()


def remove_by_username(username):
    conn = sqlite3.connect('server.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()


def deleted_users(date):
    conn = sqlite3.connect('server.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE premium_date<?", (date,))
    conn.commit()
    return cursor.fetchall()


def in_database(username, user_id):
    conn = sqlite3.connect('server.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    conn.commit()

    users_list = cursor.fetchall()
    if len(users_list) == 0:
        return False

    if users_list[0][0] is None or users_list[0][0] == user_id:
        return True

    return False


def update_user_data(username, user_id):
    conn = sqlite3.connect('server.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET user_id = ? WHERE username=?", (user_id, username))
    conn.commit()


def update_user_time(username, user_time):
    conn = sqlite3.connect('server.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET premium_date = ? WHERE username=?", (user_time, username))
    conn.commit()
