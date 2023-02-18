# Запуск проект
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
**Поднять редис в докере**
```commandline
docker-compose up -d
```
## База Данных
**Чтобы создать БД нужно выполнить SQL-инъекцию**  
**Заполнение данных происходит тоже по SQL-инъекции**
```

```
