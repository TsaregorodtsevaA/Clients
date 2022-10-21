import psycopg2

    #создание новых таблиц
def create_structure():
    cur.execute('''create table if not exists Person 
            (PersonID SERIAL Primary Key,
            name VARCHAR(60) not null,
            surname VARCHAR(60) not null,
            email VARCHAR(70) unique not null);
            
            create table if not exists Phone
            (number VARCHAR(11) UNIQUE NOT NULL Primary Key,
            PersonID int NOT NULL
            references Person(PersonID))''')

#добавление нового клиента в базу
def add_new_client(name, surname, email):
    cur.execute('''insert into Person(name, surname, email) VALUES(%s, %s, %s);''', (name, surname, email))

#добавление номера телефона
def add_phone_number(number, client_id):
    cur.execute('''insert into Phone(number, PersonID) VALUES(%s, %s);''', (number, client_id))

#Функция, позволяющая изменить данные о клиенте
def change_clients_data(PersonID, name=None, surname=None, email=None, old_phone_number=None, new_phone_number=None):
    if name!=None:
        cur.execute('''UPDATE person
        set name = %s
        where PersonID = %s;''', (name, PersonID, ))
    elif surname!= None:
        cur.execute('''UPDATE person
        set surname = %s
        where PersonID = %s;''', (surname, PersonID,))
    elif email!= None:
        cur.execute('''UPDATE person
        set email = %s
        where PersonID = %s;''', (email, PersonID,))
    elif old_phone_number!= None:
        cur.execute('''UPDATE phone
        set number = %s
        where number=%s;''', (new_phone_number, old_phone_number))
        

#Функция, позволяющая удалить телефон для существующего клиента
def delete_phone_number(phone_number):
    cur.execute('''DELETE FROM phone WHERE number=%s;''', (phone_number, ))


#Функция, позволяющая удалить существующего клиента
def delete_client(person_id):
    cur.execute('''delete from phone where PersonID=%s;
    DELETE  FROM person WHERE PersonID=%s;''', (person_id, person_id,))


#Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
def find_client(name=None, surname=None, email=None, number=None):
    cur.execute('''SELECT person.personID FROM person
    JOIN phone ph on ph.personID=person.personID
    where name=%s or surname =%s or email=%s or number=%s;''', (name, surname, email, number, ))
    print(cur.fetchone())


if __name__=="__main__":
    with psycopg2.connect(database='clients_db', user='postgres', password='postgres') as conn:
        with conn.cursor() as cur:
            create_structure()
            # add_new_client('Innokentiy', 'Petrov', 'spb@spb.ru')
            # add_new_client('Hero', 'Klin', 'ninja@gmail.com')
            # add_new_client('Mike', 'Tyson', '111@pk.com')
            # add_new_client('Vasya', 'Pupkin', 'hj@rambler.ru')
            # add_new_client('Aleksandra', 'Ivanova', 'abcde@mail.ru')
            #
            # add_phone_number('89995555555', 1)
            # add_phone_number('45654565454', 1)
            # add_phone_number('86565656565', 2)
            # add_phone_number('89997778885', 4)
            # add_phone_number('89779979752', 5)
            # add_phone_number('89779979444', 5)

            # change_clients_data('2', name= 'Hero')
            # change_clients_data('2', old_phone_number='7', new_phone_number='5')
            #
            # delete_phone_number('45654565454')
            #
            # find_client(surname='Petrov')
            # find_client(number='89997778885')
    conn.close()