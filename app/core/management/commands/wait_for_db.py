import time
from django.core.management import BaseCommand
from django.db import connections, OperationalError


class Command(BaseCommand):
    # Will pause execution until db is available

    def handle(self, *args, **options):
        self.stdout.write('Waiting for DB...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database is unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('DB is available'))
