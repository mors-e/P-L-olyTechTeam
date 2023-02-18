import re


def is_valid(email: str):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
      print("Valid email")
      return True
    else:
      print("Invalid email")
      return False


def is_valid_fio(fio: str):
    regex = re.compile(r'[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+(?:\s+[А-ЯЁ][а-яё]+)?')
    if re.fullmatch(regex, fio):
        print('Valid FIO')
        return True
    else:
        print("Invalid FIO")
        return False


def is_valid_date(data: str):
    regex = re.compile(r'(\d{2})[/.-](\d{2})[/.-](\d{4})$')
    if re.fullmatch(regex, data):
        print('Valid data')
        return True
    else:
        print("Invalid data")
        return False