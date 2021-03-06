import sqlite3


def search_ch():  # функция для получения отслеживаемых каналов
    con = sqlite3.connect("users_db.db")
    cur = con.cursor()
    result = cur.execute("""SELECT sub_chanels FROM user
                """).fetchall()
    res_ch = []
    for user in result:
        for channel in user:
            if channel not in res_ch:
                res_ch.append(channel)
    return res_ch


def search_id():  # Поиск всех канналов в дб
    con = sqlite3.connect("users_db.db")
    cur = con.cursor()
    result = cur.execute("""SELECT Name FROM user
                    """).fetchall()
    res_name = []
    for user in result:
        for channel in user:
            if channel not in res_name:
                res_name.append(channel)
    return res_name


def search_user_channels(user):  # поиск канналов определённого пользавтеля
    con = sqlite3.connect("users_db.db")
    cur = con.cursor()
    result = cur.execute(f"""SELECT sub_chanels FROM user  WHERE Name = '{user}'""").fetchall()
    result = result[0][0].split(';')
    return result


def add_info(user_id, channel):  # добавляем информацию в бд
    con = sqlite3.connect("users_db.db")
    cur = con.cursor()
    users = cur.execute(f'''SELECT Name FROM user''').fetchall()
    names = []
    for elem in users:
        names.append(str(elem[0]))
    if str(user_id) not in names:
        print(str(user_id), type(names[0]))
        cur.execute(f'''INSERT INTO user(Name, sub_chanels) VALUES ('{user_id}', '{channel}')''')
    else:
        cur.execute(f'''UPDATE user
            SET sub_chanels = '{';'.join(search_user_channels(user_id))};{channel}'
            WHERE Name = '{user_id}' ''')
    con.commit()


def del_info(user_id, channel='all'):  # удаляем информацию из бд
    con = sqlite3.connect("users_db.db")
    cur = con.cursor()
    if channel == 'all':
        cur.execute(f'''DELETE from user
            where Name == '{user_id}' ''')
    else:
        channels = search_user_channels(user_id)
        if channel in channels:
            channels.remove(channel)
            channels = ';'.join(channels)
            cur.execute(f'''UPDATE user
            SET sub_chanels = '{channels}'
            WHERE Name = '{user_id}' ''')
    con.commit()
