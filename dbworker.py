import sqlite3
import config

con = sqlite3.connect(config.db_file,check_same_thread=False)

def init_database():
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS user_city(user_id TEXT PRIMARY KEY, city_name TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS user_state(user_id TEXT PRIMARY KEY, user_current_state TEXT)")
    con.commit()
    cur.close()

def get_user_city_name(user_id):
    cur = con.cursor()
    res = cur.execute("SELECT city_name FROM user_city WHERE user_id = ?", (user_id,))
    result = res.fetchone()
    cur.close()
    return result[0]

def set_user_city(user_id, city_name):
    cur = con.cursor()
    try:
        check_res = cur.execute("SELECT user_id FROM user_city WHERE user_id = ?", (user_id,))
        exists = check_res.fetchone() is not None

        if not exists:
            cur.execute("INSERT INTO user_city(user_id, city_name) VALUES (?, ?)", (user_id, city_name))
        else:
            cur.execute("UPDATE user_city SET city_name = ? WHERE user_id = ?", (city_name, user_id))

        con.commit()
    except sqlite3.Error:
        con.rollback()
    finally:
        cur.close()

def get_user_current_state(user_id):
    cur = con.cursor()
    res = cur.execute("SELECT user_current_state FROM user_state WHERE user_id = ?", (user_id,))
    result = res.fetchone()
    cur.close()
    return result[0]


def update_user_current_state(user_id, user_current_state):
    cur = con.cursor()
    try:
        check_res = cur.execute("SELECT user_id FROM user_state WHERE user_id = ?", (user_id,))
        exists = check_res.fetchone() is not None

        if not exists:
            cur.execute("INSERT INTO user_state(user_id, user_current_state) VALUES (?, ?)", (user_id, user_current_state))
        else:
            cur.execute("UPDATE user_state SET user_current_state = ? WHERE user_id = ?", (user_current_state, user_id))

        con.commit()
    except sqlite3.Error:
        con.rollback()
    finally:
        cur.close()
