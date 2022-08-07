import json

def sing_in():
        name, password = str(input("имя: ")), str(input("пароль: "))
        file = open('users.json', 'r', encoding='utf-8') 
        data = json.load(file)
        if password == data[name]:
            print(f"Добро пожаловать {name}")
            return name
        print("не правильный пароль")
        account_action()


def registration():
        print("ВНИМАНИЕ, В ДАННОЙ ВЕРСИИ ПАРОЛИ НЕ ЗАЩИЩЕНЫ!!!")
        name, password = str(input("имя: ")), str(input("пароль: "))
        file = open('users.json', 'r', encoding='utf-8') 
        data = json.load(file)
        data[name] = password
        file.close()
        file = open('users.json', 'w', encoding='utf-8')
        json.dump(data, file)


def account_action():
    action = str(input("""
войти в аккаунт?
1 - да
2 - нет
3 - создать
"""))
    if action == "1":
        return sing_in()

    elif action == "2": pass

    elif action == "3": 
        return registration()

    else:
        print("НЕ КОРРЕКТНЫЙ ВВОД, попробуй ещё раз")
        account_action()

