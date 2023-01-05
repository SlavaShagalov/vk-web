import os
import time

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        os.system('docker-compose up -d --build')
        time.sleep(5)
        os.system('docker exec -i askme_db psql --set ON_ERROR_STOP=on --username test_user askme < askme_dump_10.sql; '
                  'docker-compose stop')
