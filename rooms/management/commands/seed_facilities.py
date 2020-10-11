from django.core.management.base import BaseCommand, CommandError
from rooms.models import Facility


class Command(BaseCommand):

    help = "Эта команда генерирует дополнительные удобства в базе данных"

    """def add_arguments(self, parser):
        parser.add_argument("--times", help="Сколько раз признаваться в любви")"""

    def handle(self, *args, **options):
        facilities = [
            "Бесплатная парковка",
            "Джакузи",
            "Спортзал",
            "Бассейн",
        ]

        for f in facilities:
            Facility.objects.create(name=f)

        self.stdout.write(self.style.SUCCESS("Дополнительные удобства созданы!"))