import random
from django.core.management.base import BaseCommand, CommandError
from django.contrib.admin.utils import flatten
from django_seed import Seed
import rooms.models as room_models
import users.models as user_models


class Command(BaseCommand):

    help = "Эта команда генерирует комнаты в базе данных"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, help="Сколько комнат создать в базе данных"
        )

    def handle(self, *args, **options):
        number = int(options.get("number"))
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(0, 500),
                "beds": lambda x: random.randint(0, 5),
                "bedrooms": lambda x: random.randint(0, 5),
                "bathrooms": lambda x: random.randint(0, 5),
                "guests": lambda x: random.randint(0, 5),
            },
        )
        created_photos = seeder.execute()
        created_clean = flatten(list(created_photos.values()))
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()

        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)
            for i in range(3, random.randint(10, 30)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    file=f"/room_photos/{random.randint(1,31)}.webp",
                    room=room,
                )
            for a in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(a)

            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)

            for r in rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(r)

        self.stdout.write(self.style.SUCCESS(f"{number} комнат создано"))
