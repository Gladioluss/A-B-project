import os
import string
import random
import requests
from transliterate import translit
from tkinter import *


TOKEN = None
DOMAIN = None
USER_AGENT = "ipangt"


def pars_token_and_domain():
    with open('token_and_domain.txt', 'r') as txt:
        arr = []
        for line in txt:
            arr.append(line.split(':'))
        global TOKEN, DOMAIN
        TOKEN = arr[0][1].strip().strip('\n')
        DOMAIN = arr[1][1].strip().strip('\n')


def create_nickname():
    message = '''
    Почта составленная из ваших инициалов уже зарегистрирована,
    поэтому придумайте и введите её вручную: '''
    nk = Tk()
    nk.title("Entry Fullname")
    nk.geometry("400x250")
    label1 = Label(nk, text=message)
    label1.place(relx=.0, rely=.1)
    label1.pack()
    message_entry = Entry(nk)
    message_entry.place(relx=.5, rely=.1)
    message_entry.pack()
    button_enter = Button(nk, text="Ввести", command=nk.quit)
    button_enter.place(relx=.5, rely=.4)
    button_enter.pack()

    nk.mainloop()
    return str(message_entry.get())


def load_user():
    root = Tk()
    root.title("Entry Fullname")
    root.geometry("300x250")
    first = StringVar()
    last = StringVar()
    middle = StringVar()

    first_label = Label(text="Введите имя:")
    last_label = Label(text="Введите фамилию:")
    middle_label = Label(text="Введите Отчество:")

    first_label.grid(row=0, column=0, sticky="w")
    last_label.grid(row=1, column=0, sticky="w")
    middle_label.grid(row=2, column=0, sticky="w")

    first_entry = Entry(textvariable=first)
    last_entry = Entry(textvariable=last)
    middle_entry = Entry(textvariable=middle)

    first_entry.grid(row=0, column=1, padx=5, pady=5)
    last_entry.grid(row=1, column=1, padx=5, pady=5)
    middle_entry.grid(row=2, column=1, padx=5, pady=5)

    message_button = Button(text="Ввести", command=root.quit)
    message_button.grid(row=3, column=1, padx=5, pady=5, sticky="e")

    root.mainloop()
    return {
        'first': str(first.get()),
        'last': str(last.get()),
        'middle': str(middle.get()),
    }


def get_nickname(data):
    return translit(data['last'].strip()[0].lower()
                    + data['first'].strip()[0].lower()
                    + data['middle'].strip()[0].lower(),
                    language_code='ru', reversed=True)


def get_fullname(data):
    return '{0} {1} {2}'.format(data['last'].strip(), data['first'].strip(), data['middle'].strip())


def create_user(data):
    data = {
        key: value.strip()
        for key, value in data.items()
    }

    department_id = 1
    if len(data) != 5:
        nickname = get_nickname(data)
    else:
        nickname = data['nickname']
    payload = {
        'nickname': nickname,
        'name': {
            'first': data['first'],
            'last': data['last'],
            'middle': data['middle']
        },
        'department_id': department_id,
        'password': data['password'],
    }
    headers = {
        'Authorization': 'OAuth ' + TOKEN,
        'User-Agent': USER_AGENT,
    }
    response = requests.post(
        'https://api.directory.yandex.net/v6/users/',
        json=payload,
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()
    response_data = response.json()
    return [response_data['id'], nickname]


def create_random_password(length=10):
    symbols = string.ascii_letters + string.digits
    return ''.join(
        random.choice(symbols)
        for i in range(length)
    )


def load_already_created():

    params = {
        'fields': 'nickname',
    }
    headers = {
        'Authorization': 'OAuth ' + TOKEN,
        'User-Agent': USER_AGENT,
    }

    response = requests.get(
        'https://api.directory.yandex.net/v6/users/',
        params=params,
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()
    response_data = response.json()
    results = response_data['result']
    return {user['nickname'] for user in results}


def create_users(output):

    if os.path.exists(output):
        raise RuntimeError('Файл {0} существует. Выберите другое имя файла.')

    user_data = load_user()
    already_created = load_already_created()

    new_user = ''

    try:
        fullname = get_fullname(user_data)
        nickname = get_nickname(user_data)
        user_data['password'] = create_random_password()
        if nickname in already_created:
            nickname = create_nickname()
            user_data['nickname'] = nickname
        create_user(user_data)
        new_user = (fullname, user_data['password'], nickname)
    except Exception:
        print('Не получилось завести сотрудника: {0}'.format(user_data))

    if new_user:

        with open(output, 'w') as output_file:
            output_file.write('fullname,password,emailAddress\n')
            output_file.writelines(
                '{0},{1},{2}\n'.format(new_user[0], new_user[1], new_user[2]+DOMAIN)
            )
            output_file.close()
    return new_user


if __name__ == '__main__':
    #print(eval(input()))
    pars_token_and_domain()
    create_users('passwords.csv')

#len([7, 7, 4])