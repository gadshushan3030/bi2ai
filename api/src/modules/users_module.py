import pymysql.cursors
import pymysql


def get_by_username(username):
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='3038',
                                 db='bi2ai',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE username = %s LIMIT 1"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    return user


def set_token(token, user_id):
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='3038',
                                 db='bi2ai',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    query = " UPDATE users SET access_token = %s WHERE user_id = %s"
    val = (token, user_id)
    cursor.execute(query, val)
    connection.commit()
