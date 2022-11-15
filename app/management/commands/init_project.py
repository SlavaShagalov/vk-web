import os

from django.core.management.base import BaseCommand
from app.models import Profile
from django.contrib.auth.models import User


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # os.system('docker-compose up -d --build')
        # os.system('python manage.py migrate')
        # os.system('python manage.py makemigrations app')
        # os.system('python manage.py migrate')
        # print('Load DB data...')
        # os.system('python manage.py loaddata app -o db.json')
        # print('Success.')

        self.create_admin()

        # os.system('docker-compose stop')

    def create_admin(self):
        print('Create admin...')
        os.system(
            'DJANGO_SUPERUSER_PASSWORD=1234 '
            'python manage.py createsuperuser --username admin '
            '--email admin@email.com '
            '--noinput')
        admin = User.objects.get(username='admin')
        admin.first_name = 'Admin'
        admin.last_name = 'Adminov'
        admin.save()
        profile = Profile(user=admin)
        profile.save()
        print('Success.')
