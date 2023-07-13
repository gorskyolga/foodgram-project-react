# praktikum_new_diplom
DOMAIN: simpletaski.hopto.org
SUPERUSER:
- login: olga_admin
- password: password&79


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
docker compose -f docker-compose.production.yml up
docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic --noinput
docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /app/backend_static/
docker compose -f docker-compose.production.yml exec backend python manage.py migrate

```
4. Создать суперюзера
```
docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
```
5. Наполнить базу тестовыми данными
```
docker compose -f docker-compose.production.yml exec backend python manage.py import_ingredients
docker compose -f docker-compose.production.yml exec backend python manage.py add_initial_data
```
6. Доступные эндпоинты в API описаны http://localhost/api/docs/