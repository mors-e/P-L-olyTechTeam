# Проект
## Функциональность
***Реализованно:***
- **Чат с HR-отделом**
- **Анкета после 1 недели** 
- **Пример чекпоинта (презентация)**
- **Регистация пользователей**
  
  
## Особенности
***Особенность проекта в следующем:***
- **Прямой чат в боте (в будующем не только HR-отдел, но и с руководителем проекта)**
- **Показ презентаций в чате, опрос по пройденной информации**
- **Кросспратформенность**
- **Закрытая экосисестема для работников компании**

## Стек технологий
  
- **python**
- **aiogram**
- **docker**
- **redis**
- **MySQL**

## Демо
***Демо сервиса доступно по адресу: https://t.me/LolyTech_bot***  
Пока запущено на localhost, но в дальнейшем будет загружен на постоянный сервер

Если у вы пытаесь ввести команду или сообщение, но ничего не происходит  
то есть 2 варианта:
- Вы находитесь в состоянии заполнения формы, чтобы выйти введите команду  `/cancel`
- Эта функция не работает => и была запущена форма состояния => пишем `/cancel`

## Запуск проект
**Создать вирутальную среду**   
```commandline
python -m venv env
```
**Активировать env**  
***- для Windows***
```commandline
venv\Scripts\activate.bat
```
***- для Linux и MacOS***
```commandline
. venv/bin/activate
```
**Установка библиотек**
```commandline
pip install -r requirements.txt
```  
***Следует создать файл .env для переменных окружения***  
Примерное наполнение env файла:  
```commandline
TOKEN=your_token_api_telegram

HOST=localhost
PORT=3306
USER=root
PASSWORD=root
DATABASE=xakaton
```

**Поднять редис в докере**
```commandline
docker-compose up -d
```
## База Данных
**Чтобы создать БД нужно выполнить SQL файл** `shema.sql`  
Заполнение БД происходит с помощью админа, чтобы получить админ статус напишите чату:  
```
/admin_status
```
Данная команда позволяет обрабатывать анкеты (принимать и отклонять пользователей)