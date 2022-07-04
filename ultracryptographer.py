#где-то здесть будут библиотеки
import math
import random
import qrcode  

##### НАСТРОЙКИ И ФОРМАТИРОВАНИЕ #####
all_alphabets = {
                1: "абвгдеёжзийклмнопрстуфхцчшщъыьэюя ",
                2: "abcdefghijklmnopqrstuvwxyz ",
                3: "аәбвгғдеёжзийкқлмнңоөпрстуұүфхһцчшщъыіьэюя ", 
                4: "abcdefghijklmnñopqrstuvwxyz ",
                4444: "здесь был DANIRU"
                }
marks = {
        ",": "зпт",
        ".": "тчк",
        "?": "впрс",
        "1": "одиин",
        "2": "двва",
        "3": "трри",
        "4": "четыыре",
        "5": "пяять",
        "6": "шеесть",
        "7": "сеемь",
        "8": "воссемь",
        "9": "деввять",
        "0": "нооль"   
        }

alphabet, word_to_index, index_to_word  = "", "", ""

def alphabets():
    global alphabet
    global word_to_index
    global index_to_word
    alphabet = int(input("""
Какой язык изспользовать?  
1 - русский
2 - английский  
3 - казахский
4 - испанский
ввод:"""))
    alphabet = all_alphabets.get(alphabet) 
    word_to_index = dict(zip(alphabet, range(len(alphabet))))
    index_to_word = dict(zip(range(len(alphabet)), alphabet))

def replase_mark(message): # заменяем запятую и точку на зпт и тчк 
    global marks
    for i in marks.keys():
        message = message.replace(i, marks.get(i))
    return message

def antireplase_mark(decrypted): #восстанавливаем запятые и точки из зпт и тчк
    global marks
    for i in marks.keys():
        decrypted = decrypted.replace(marks.get(i), i)
    return decrypted
    
def filtering_text(message): #убирает все символы не входящие в алфавит и заменяет на пробел
    message = message.lower()
    for word in range(len(message)):
        if message[word] not in alphabet: 
            message = message.replace(message[word], " ")
    return message 

def full_preprocessing(message): #не работает с другими языками кроме русского
    return filtering_text(replase_mark(message))

def key_choise():
    global alphabet
    key_choise = int(input(f"""
введи ключ из неповторяющихся букв длинной {len(alphabet)-1} или дай сделать это мне
1 - ручной ввод
2 - сгенерировать
ввод: """))

    if key_choise == 1:
        key = input("введи ключ: ")

    elif key_choise == 2:
        key = list(alphabet)
        random.shuffle(key)
        key = "".join(key) 
        print(key)
    return key  

def mega_key_choise(message):
    global alphabet
    key_choise = int(input(f"""
введи ключ из букв длинной до {len(message)} или дай сделать это мне
1 - ручной ввод
2 - сгенерировать
ввод: """))

    if key_choise == 1:
        key = input("введи ключ: ")

    elif key_choise == 2:
        key = []
        while len(key) < len(message):
            key.append(random.choice(list(alphabet)))
        key = "".join(key) 
        print(key)
    return key  

def save_result(*anything):
    save_file = int(input("""
сохранить текст и ключ в файле?
1 - да
2 - нет
ввод: """))
    if save_file == 1:
        with open('crypto.txt','a', encoding='utf-8') as crypto_text:
            crypto_text.write(f"{anything}\n")
    save_qr = int(input("""
а в формате QR кода?
1 - да 
2 - нет
ввод: """))
    if save_qr == 1:
        img = qrcode.make(anything)
        img.save(f'crypto{random.randint(1,4444)}.png')

    
##### ШИФРЫ #####

#ОБРАТНЫЙ ШИФР
def reverse_cipher():
    message = input("введи текст: ")
    reverse_message = ''
    len_mes = len(message) - 1
    while len_mes >= 0:
        reverse_message = reverse_message + message[len_mes]
        len_mes -= 1
    print(reverse_message)
    return reverse_message


def caesar_cipher():
    alphabets()
    print("""
выбери действие 
1 - зашифровать 
2 - расшифровать
3 - взломать""")

    choice_mode = int(input("ввод: "))
    message = full_preprocessing(input("введи текст: ")) 
    
    if choice_mode != 3:
        cipher = ""
        shift = int(input("введи смещение: "))
        if choice_mode == 1:
            cipher = ''.join([index_to_word[(word_to_index[word] + shift) % len(word_to_index)] for word in message])
        elif choice_mode == 2:
            cipher = ''.join([index_to_word[(word_to_index[word] - shift) % len(word_to_index)] for word in cipher])
            antireplase_mark(cipher)
        print(cipher)
        return cipher, shift

    elif choice_mode == 3: #все переделать, основываться на частотности (хотя можно и оставить)
        all_comb = []
        for shift in range(len(alphabet)+1):
            breaking = ''
            for letter in message:
                number = (word_to_index[letter] - shift) % len(word_to_index)
                letter = index_to_word[number]
                breaking += letter
            all_comb.append(breaking)
        print(antireplase_mark('\n'.join(all_comb)))       
        return antireplase_mark('\n'.join(all_comb))


def permutation_cipher():
    print("""
выбери действие 
1 - зашифровать 
2 - расшифровать
3 - взломать""")
    choice_mode = int(input("ввод: "))
    message = input("введи текст: ")

    if choice_mode == 1:    #попытаться переделать через транспонирование матрицы (или нет)
        key = int(input(f"введи ключ от 2 до {len(message)//2 + 1}: "))
        cipher = [''] * key
        for column in range(key):       
            currentindex = column
            while currentindex < len(message):
                cipher[column] += message[currentindex]
                currentindex += key
        print("".join(cipher))
        return "".join(cipher), key 

    elif choice_mode == 2: 
        key = int(input(f"введи ключ от 2 до {len(message)//2 + 1}: "))
        num_columns, num_rows = int(math.ceil(len(message) / float(key))), key
        num_zoro = (num_columns * num_rows) - len(message)
        decrypted = [''] * num_columns
        column, row = 0, 0
        for sumbol in message:
            decrypted[column], column = decrypted[column] + sumbol, column + 1
            if (column == num_columns) or (column == num_columns - 1 and row >= num_rows - num_zoro):
                column, row = 0, row + 1
        print(''.join(decrypted))
        return ''.join(decrypted), key

    elif choice_mode == 3: 
        message, all_comb = message[:len(message)-1], []
        for key in range(2, len(message)//2 + 1):
            num_columns, num_rows = int(math.ceil(len(message) / float(key))), key
            num_zoro = (num_columns * num_rows) - len(message)
            decrypted = [''] * num_columns
            column, row = 0, 0
            for sumbol in message:
                decrypted[column], column = decrypted[column] + sumbol, column + 1
                if (column == num_columns) or (column == num_columns - 1 and row >= num_rows - num_zoro):
                    column, row = 0, row + 1
            all_comb.append(''.join(decrypted))
        print('\n'.join(all_comb))
        return '\n'.join(all_comb)


def substitution_cipher():
    global alphabet
    alphabets() 
    print("""
выбери действие 
1 - зашифровать 
2 - расшифровать""")
    choice_mode = int(input("ввод: "))
    message, key = full_preprocessing(input("введи текст: ")), key_choise()
    if choice_mode == 1:
        cipher = ''
        for sumbol in message:
            sumbol_ind = alphabet.find(sumbol)
            cipher += key[sumbol_ind]
        print(cipher)
        return cipher, key
             
    elif choice_mode == 2:
        alphabet, key, decrypted = key, alphabet, ''
        for sumbol in message:
            sumbol_ind = alphabet.find(sumbol)
            decrypted += key[sumbol_ind]
        print(antireplase_mark(decrypted))
        return antireplase_mark(decrypted), key
        
    
def vigenere_cipher():
    global alphabet
    alphabets() 
    print("""
выбери действие 
1 - зашифровать 
2 - расшифровать""")
    choice_mode = int(input("ввод: "))
    message, key_index, cipher = full_preprocessing(input("введи текст: ")), 0, []
    key = mega_key_choise(message)
    for symbol in message:
        num = alphabet.find(symbol)
        if num != -1:
            if choice_mode == 1:
                num += alphabet.find(key[key_index])
            elif choice_mode == 2:
                num -= alphabet.find(key[key_index])
            
            num %= len(alphabet)
            cipher.append(alphabet[num])
            key_index += 1

            if key_index == len(key):
                key_index = 0
    print(antireplase_mark(''.join(cipher)))
    return antireplase_mark(''.join(cipher)), key 

def main():
    while True:
        try:
            print('''       
       Powered by DANIRU44
            alpha 1.0.3  
                                 ''')
                                        
            print('''
Выберите шифр:
1 - Обратный шифр
2 - Шифр Цезаря
3 - Перестановочный шифр
4 - Подстановочный  шифр
5 - Шифр Виженера''')

            type_cipher = int(input('ввод: '))
            if type_cipher == 1:
                save_result(reverse_cipher()) #готов
            elif type_cipher == 2:
                save_result(caesar_cipher()) #готов (ведуться работы по улучшению взлома)
            elif type_cipher == 3:
                save_result(permutation_cipher()) #готов
            elif type_cipher == 4:
                save_result(substitution_cipher())#готов
            elif type_cipher == 5:
                save_result(vigenere_cipher())#готов

        except:
            print("""
    ЧТО-ТО ПОШЛО НЕ ТАК, вводи корректные значения""")

        finally:
            vihod = int(input("""
продолжить? 
1 - да 
любая другая кнопка - нет
ввод: """))
            if vihod != 1:
                break

if __name__ == "__main__":
    main()

#Это текст для отладки 1234. Всё должно быть на своих местах, кроме этого hello world. 