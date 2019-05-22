from django.core import exceptions
from django.core.management.base import BaseCommand, CommandError
import pandas as pd
import os
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):

        url = os.path.join(settings.BASE_DIR, '/docs/k8s_resource.csv')
        df = pd.read_csv(url)


