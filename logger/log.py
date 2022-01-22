import datetime

import colorama

colorama.init()


def getmonth(n):
    return ['January',
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
            ][n - 1]


def save_to_log(string):
    date = datetime.datetime.now()
    try:
        with open('log_{}_{}.txt'.format(date.year, getmonth(date.month)), 'a', encoding="utf-8") as file:
            file.write(string + '\n')
    except:
        pass
    return str(string)


def warning(text):
    print(colorama.Fore.RED, save_to_log(get_date() + str(text)), sep='')


def notice(text):
    print(colorama.Fore.YELLOW, save_to_log(get_date() + str(text)), sep='')


def log(text):
    print(colorama.Fore.CYAN, save_to_log(get_date() + str(text)), sep='')


def discrete(text):
    print(colorama.Fore.LIGHTBLACK_EX, save_to_log(get_date() + str(text)), sep='')


def third_party(text):
    print('\033[92m', save_to_log(get_date() + str(text)), '\033[0m', sep='')


def get_date():
    return datetime.datetime.now().strftime("[%Y-%m-%d - %H:%M:%S.%f] - ")


class Log:
    def __init__(self, name, form="[{}] {}"):
        self.name = name
        self.form = form

    def warning(self, text):
        warning(self.form.format(self.name, text))

    def notice(self, text):
        notice(self.form.format(self.name, text))

    def log(self, text):
        log(self.form.format(self.name, text))

    def discrete(self, text):
        discrete(self.form.format(self.name, text))

    def third_party(self, text):
        third_party(self.form.format(self.name, text))
