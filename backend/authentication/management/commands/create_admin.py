from django.core.management.base import BaseCommand
from authentication.models import User

class Command(BaseCommand):
    help = 'Create the default admin user'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='benjamin').exists():
            User.objects.create_superuser(
                username='benjamin',
                password='benjamin',
                email='admin@example.com',
                role='admin'
            )
            self.stdout.write(self.style.SUCCESS('Admin user created successfully.'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists.'))
