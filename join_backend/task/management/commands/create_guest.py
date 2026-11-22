from django.core.management.base import BaseCommand

from task.models import CustomUser

GUEST_EMAIL = 'guest@guest.com'
GUEST_PASSWORD = '123'  # öffentlich bekannt: Gast-Login auf der Startseite


class Command(BaseCommand):
    help = 'Legt das Gast-Konto für den "Guest Log in" an (falls es noch nicht existiert).'

    def handle(self, *args, **options):
        user, created = CustomUser.objects.get_or_create(
            email=GUEST_EMAIL,
            defaults={'user_name': 'Guest', 'initials': 'G', 'color': '#2A3647'},
        )
        if created:
            user.set_password(GUEST_PASSWORD)
            user.save()
            self.stdout.write(self.style.SUCCESS('Gast-Konto angelegt.'))
        else:
            self.stdout.write('Gast-Konto existiert bereits.')
