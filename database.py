mysql = None

def set_database(mysql_instance):
    global mysql
    mysql = mysql_instance

def get_connection():
    return mysql.connection if mysql else None

def get_cursor():
    connection = get_connection()
    return connection.cursor() if connection else None

def execute(query, params=()):
    cur = get_cursor()
    if cur:
        cur.execute(query, params)
        return cur
    return None

def fetchone(query, params=()):
    cur = execute(query, params)
    return cur.fetchone() if cur else None

def fetchall(query, params=()):
    cur = execute(query, params)
    return cur.fetchall() if cur else []
