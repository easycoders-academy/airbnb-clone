from django.core.management.base import BaseCommand, CommandError
from rooms.models import Amenity


class Command(BaseCommand):

    help = "Эта команда генерирует удобства в базе данных"

    """def add_arguments(self, parser):
        parser.add_argument("--times", help="Сколько раз признаваться в любви")"""

    def handle(self, *args, **options):
        amenities = [
            "Кухня",
            "Отопление",
            "Стиральная машина",
            "Wi-Fi",
            "Камин",
            "Утюг",
            "Место для работы на ноутбуке",
            "Кроватка",
            "Самостоятельное прибытие",
            "Датчик угарного газа",
            "Береговая линия",
            "Шампунь",
            "Кондиционер",
            "Сушильная машина",
            "Завтрак",
            "Плечики",
            "Фен",
            "Телевизор",
            "Стул для кормления",
            "Датчик дыма",
            "Отдельная ванная комната",
            "У воды",
        ]

        for a in amenities:
            Amenity.objects.create(name=a)

        self.stdout.write(self.style.SUCCESS("Удобства созданы!"))