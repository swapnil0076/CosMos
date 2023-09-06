from django.core.management.base import BaseCommand
import subprocess

class Command(BaseCommand):
    help = 'Starts the Streamlit app'

    def handle(self, *args, **options):
        try:
            subprocess.run(['streamlit', 'run', 'views.py'])
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('Streamlit app stopped by user'))
