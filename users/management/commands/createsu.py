from django.core.management.base import BaseCommand, CommandError
from users.models import User


class Command(BaseCommand):

    help = "Эта команда генерирует суперпользователя"

    def handle(self, *args, **options):
        admin = User.objects.get_or_none(username="ebadmin")
        if not admin:
            User.objects.create_superuser(
                "ebadmin", "maxilead.agency@gmail.com", "123456"
            )
            self.stdout.write(self.style.SUCCESS(f"Администратор создан"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Администратор уже создан"))
