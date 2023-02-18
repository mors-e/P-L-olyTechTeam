# Запуск проект
**Создать вирутальную среду**   
```python
python -m venv env
```
**Активировать env**  
***- для Windows***
```python
venv\Scripts\activate.bat
```
***- для Linux и MacOS***
```python
. venv/bin/activate
```
**Установка библиотек**
```python
pip install -r requirements.txt
```
**Поднять редис в докере**
```python
docker-compose up -d
```
