import random
from django.core.management.base import BaseCommand, CommandError
from django.contrib.admin.utils import flatten
from django_seed import Seed
import lists.models as lists_models
import users.models as users_models
import rooms.models as rooms_models


class Command(BaseCommand):

    help = "Эта команда генерирует списки в базе данных"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, help="Сколько списков создать в базе данных"
        )

    def handle(self, *args, **options):
        number = int(options.get("number"))
        user = users_models.User.objects.all()
        room = rooms_models.Room.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            lists_models.List,
            number,
            {
                "user": lambda x: random.choice(user),
            },
        )
        created = seeder.execute()
        clean = flatten(list(created.values()))
        for pk in clean:
            list_model = lists_models.List.objects.get(pk=pk)
            to_add = room[random.randint(0, 5) : random.randint(6, 30)]
            list_model.rooms.add(*to_add)

        self.stdout.write(self.style.SUCCESS(f"{number} списков создано"))
