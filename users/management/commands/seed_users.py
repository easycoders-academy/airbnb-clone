from django.core.management.base import BaseCommand, CommandError
from django_seed import Seed
from users.models import User


class Command(BaseCommand):

    help = "Эта команда генерирует пользователей в базе данных"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, help="Сколько пользователей создать в базе данных"
        )

    def handle(self, *args, **options):
        number = int(options.get("number"))
        seeder = Seed.seeder()
        seeder.add_entity(User, number, {"is_staff": False, "is_superuser": False})
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} пользователей создано"))
