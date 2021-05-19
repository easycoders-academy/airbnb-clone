from django.core.management.base import BaseCommand, CommandError
from rooms.models import RoomType


class Command(BaseCommand):

    help = "Эта команда генерирует Типы жилья в базе данных"

    """def add_arguments(self, parser):
        parser.add_argument("--times", help="Сколько раз признаваться в любви")"""

    def handle(self, *args, **options):
        room_types = [
            "Жилье целиком",
            "Отдельная комната",
            "Гостиничный номер",
            "Место в комнате",
        ]

        for f in room_types:
            RoomType.objects.create(name=f)

        self.stdout.write(self.style.SUCCESS("Типы жилья созданы!"))
