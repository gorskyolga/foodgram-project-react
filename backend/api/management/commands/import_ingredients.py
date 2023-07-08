import csv
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = ('Импорт ингредиентов из csv-файла в БД.')

    def handle(self, *args, **options):
        self.stdout.write('Импорт ингредиентов...')
        with open('/app/data/ingredients.csv', encoding='utf-8') as csv_file:
            for row in csv.DictReader(
                csv_file, delimiter=',', fieldnames=['ingredient', 'unit']
            ):
                Ingredient.objects.get_or_create(
                    name=row['ingredient'], measurement_unit=row['unit']
                )
        self.stdout.write('Ингредиенты загружены.')
