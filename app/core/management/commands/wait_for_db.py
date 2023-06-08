"""
Django Command to wait for the Database to be available
"""

from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psycopg20Error
from django.db.utils import OperationalError
import time


class Command(BaseCommand):
    """Django Command to wait for Database"""
    def handle(self, *args, **options):
        """ Entry Points for Commands."""
        self.stdout.write('waiting for database....')
        db_up = False
        while(db_up is False):
            try:
                self.check(databases=['default'])
                db_up = True
            except(Psycopg20Error, OperationalError):
                self.stdout.write('Database is unavailable awaiting 1 sec ..')
                time.sleep(1)   
        self.stdout.write(self.style.SUCCESS('Database is available'))