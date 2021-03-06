import pymysql
import time
from random import Random
from bili_spider.config import dbconfig

# 创建连接
conn = pymysql.connect(**dbconfig)

# 创建游标
cursor = conn.cursor()


def random_str(random_length=8):
    str1 = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str1 += chars[random.randint(0, length)]
    return str1


def insert_user(data=None):
    if data == {} or (data['name'] == 'None') or (data['name'] == ''):
        data['name'] = random_str()
    else:
        data['add_time'] = time.time()
    sql = 'insert into user_info set '
    for key in data.keys():
        sql += ' ' + str(key) + ' = \'' + str(data[key]) + '\' ,'
    sql = sql.rstrip(',')
    cursor.execute(sql)
    conn.commit()
    return cursor.lastrowid


def insert_extend_user(user_id=0, data=None):
    if not data:
        data = {'user_id': user_id}
    else:
        data['user_id'] = user_id
        data['add_time'] = time.time()
    sql = 'insert into extend_info set '
    for key in data.keys():
        sql += ' ' + str(key) + ' = \'' + str(data[key]) + '\' ,'
    sql = sql.rstrip(',')
    cursor.execute(sql)
    conn.commit()


def update_user(user_id=0, data=None):
    if (data['name'] == 'None') or (data['name'] == ''):
        data = {'name': random_str()}
    else:
        data['add_time'] = time.time()
    sql = 'update user_info set '
    for key in data.keys():
        sql += ' ' + str(key) + ' = \'' + str(data[key]) + '\' ,'
    sql = sql.rstrip(',') + 'where id = ' + str(user_id)
    # print(sql)
    cursor.execute(sql)
    conn.commit()


def update_extend_user(user_id=0, data=None):
    if not data:
        pass
    else:
        data['add_time'] = time.time()
    sql = 'update  extend_info set '
    for key in data.keys():
        sql += ' ' + str(key) + ' = \'' + str(data[key]) + '\' ,'
    # print(sql)
    sql = sql.rstrip(',') + 'where user_id = ' + str(user_id)
    cursor.execute(sql)
    conn.commit()


def get_fail_user():
    sql = 'select id from user_info where  register_time = 0 and level = 0 and location != \'未填写\''
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    return result


def delete_fail_user():
    sql = "delete from user_info where  register_time = 0 and level = 0  and location != '未填写'"
    sql_2 = "DELETE FROM extend_info WHERE `head_img` = ''"
    cursor.execute(sql)
    result = cursor.rowcount
    cursor.execute(sql_2)
    conn.commit()
    return result


def get_next_id():
    sql = "select max(id) from user_info"
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.commit()
    return result[0] + 1


def close():
    cursor.close()
    conn.close()

