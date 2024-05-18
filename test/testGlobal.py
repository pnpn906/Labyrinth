
users = ["us1", "us2"]
print(users)

def clear_users():
    users = []  # это другая переменная - не та, которая выше, присваивать значения переменным за пределами функций нельзя

def clear_users2():
    global users    # а если указать явно, что мы хотим с ней работать, то можно будет менять
    users = []

def show_users():
    global users # и без этого работать будет, просто рекомендация
    for user in users:  # а вот просматривать можно
        print(user)

clear_users()
print(users)
clear_users2()
print(users)
show_users()