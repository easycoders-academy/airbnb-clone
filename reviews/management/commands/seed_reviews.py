import random
from django.core.management.base import BaseCommand, CommandError
from django_seed import Seed
import reviews.models as review_models
import users.models as users_models
import rooms.models as rooms_models


class Command(BaseCommand):

    help = "Эта команда генерирует отзывы в базе данных"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, help="Сколько отзывов создать в базе данных"
        )

    def handle(self, *args, **options):
        number = int(options.get("number"))
        user = users_models.User.objects.all()
        room = rooms_models.Room.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            review_models.Review,
            number,
            {
                "cleanliness": lambda x: random.randint(0, 6),
                "communication": lambda x: random.randint(0, 6),
                "checkin": lambda x: random.randint(0, 6),
                "accuracy": lambda x: random.randint(0, 6),
                "location": lambda x: random.randint(0, 6),
                "value": lambda x: random.randint(0, 6),
                "user": lambda x: random.choice(user),
                "room": lambda x: random.choice(room),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} отзывов создано"))
