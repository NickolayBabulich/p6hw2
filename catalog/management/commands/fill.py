from django.core.management import BaseCommand

from catalog.models import Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        category_list = [
            {'name': 'Компьютер', 'description': 'Компьютер'},
            {'name': 'Принтер', 'description': 'Принтер'},
            {'name': 'Пылесос', 'description': 'Пылесос'},
            {'name': 'Холодильник', 'description': 'Холодильник'},
            {'name': 'Телевизор', 'description': 'Телевизор'},
        ]

        category_for_create = []
        for category_item in category_list:
            category_for_create.append(
                Category(**category_item)
            )
        if not Category.objects.all():
            Category.objects.bulk_create(category_for_create)
        else:
            Category.objects.all().delete()
            Category.objects.bulk_create(category_for_create)
