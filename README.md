# praktikum_new_diplom

# Как работать с репозиторием финального задания
1. Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/gorskyolga/foodgram-project-react.git
cd foodgram-project-react
```
2. Создать файл .env в корне проекта
```
touch .env
```
И описать в нем переменные по примеру файла .env.example
3. Запустить проект локально в контейнерах:
```
cd /c/Dev/foodgram-project-react/infra
docker compose up
```
4. Скопировать статику
```
docker compose exec backend cp -r /app/collected_static/. /app/backend_static/
```
5. Создать суперюзера
```
docker compose exec backend python manage.py createsuperuser
```
6. Наполнить базу тестовыми данными
```
docker compose exec backend python manage.py import_ingredients
docker compose exec backend python manage.py add_initial_data
```
7. Доступные эндпоинты в API описаны http://localhost/api/docs/