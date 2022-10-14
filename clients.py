import psycopg2

with psycopg2.connect(database = 'clients_db', user = 'postgres', password = 'postgres') as conn:

    with conn.cursor() as cur:
        cur.execute('''drop table Phone''')
    with conn.cursor() as cur:
        cur.execute('''drop table Person''')

    #создание новых таблиц
    def create_structure(new_table_name, colomn_info):
        with conn.cursor() as cur:
            cur.execute(f'''create table if not exists {new_table_name}
                        ({colomn_info});''')
            conn.commit()
    create_structure('Person', '''PersonID SERIAL Primary Key,
                               name VARCHAR(60) not null, 
                               surname VARCHAR(60) not null,
                               email VARCHAR(70) unique not null''')
    create_structure('Phone', '''number VARCHAR(11) UNIQUE NOT NULL Primary Key,
                                PersonID int NOT NULL references Person(PersonID)''')

    #добавление нового клиента в базу
    def add_new_client(name, surname, email):
        with conn.cursor() as cur:
            cur.execute('''insert into Person(name, surname, email)
            VALUES(%s, %s, %s);''', (name, surname, email))
            conn.commit()
    add_new_client('Innokentiy', 'Petrov', 'spb@spb.ru')
    add_new_client('Hero', 'Klin', 'ninja@gmail.com')
    add_new_client('Mike', 'Tyson', '111@pk.com')
    add_new_client('Vasya', 'Pupkin', 'hj@rambler.ru')
    add_new_client('Aleksandra', 'Ivanova', 'abcde@mail.ru')



    #добавление номера телефона
    def add_phone_number(number, client_id):
        with conn.cursor() as cur:
            cur.execute('''insert into Phone(number, PersonID)
            VALUES(%s, %s);''', (number, client_id))
            conn.commit()
    add_phone_number('89995555555', 1)
    add_phone_number('45654565454', 1)
    add_phone_number('86565656565', 2)
    add_phone_number('89997778885', 4)
    add_phone_number('89779979752', 5)
    add_phone_number('89779979444', 5)


    #Функция, позволяющая изменить данные о клиенте
    def change_clients_data(table, colomn_to_change, primary_key_colomn, new_info, primary_key_info):
        with conn.cursor() as cur:
            cur.execute(f'''UPDATE {table} set {colomn_to_change}=%s where {primary_key_colomn}=%s;
            ''', (new_info, primary_key_info))
            conn.commit()
    # change_clients_data('Person', 'Email', 'PersonID', 'changed@yes.com', 1)
    # change_clients_data('Phone', 'number', 'number', '555', '45654565454')


    #Функция, позволяющая удалить телефон для существующего клиента
    def delete_phone_number(phone_number):
        with conn.cursor() as cur:
            cur.execute('''DELETE FROM phone WHERE number=%s;''', (phone_number, ))
            conn.commit()
    #delete_phone_number('45654565454')


    #Функция, позволяющая удалить существующего клиента
    def delete_client(person_id):
        with conn.cursor() as cur:
            cur.execute('''delete from phone where PersonID=%s;
            DELETE  FROM person WHERE PersonID=%s;''', (person_id, person_id,))
            conn.commit()
    #delete_client(1)


    #Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
    def find_client(colomn, info):
        with conn.cursor() as cur:
            cur.execute(f'''SELECT person.personID FROM person
            JOIN phone ph on ph.personID=person.personID
            where {colomn}=%s;''', (info,))
            print(cur.fetchone())
    # find_client('name', 'Hero')
    # find_client('number', '89997778885')
