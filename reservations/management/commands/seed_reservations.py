import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from django_seed import Seed
import reservations.models as reservations_models
import users.models as users_models
import rooms.models as rooms_models


class Command(BaseCommand):

    help = "Эта команда генерирует бронирования в базе данных"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, help="Сколько бронирований создать в базе данных"
        )

    def handle(self, *args, **options):
        number = int(options.get("number"))
        user = users_models.User.objects.all()
        room = rooms_models.Room.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            reservations_models.Reservation,
            number,
            {
                "status": lambda x: random.choice(["pending", "confirmed", "canceled"]),
                "guest": lambda x: random.choice(user),
                "room": lambda x: random.choice(room),
                "check_in": lambda x: datetime.now(),
                "check_out": lambda x: datetime.now()
                + timedelta(days=random.randint(3, 25)),
            },
        )
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{number} бронирований создано"))
