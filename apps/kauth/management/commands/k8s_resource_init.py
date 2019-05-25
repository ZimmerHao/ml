from django.core.management.base import BaseCommand
import pandas as pd
import os
from django.conf import settings

from apps.kauth.models import KResource


class Command(BaseCommand):

    def handle(self, *args, **options):

        url = os.path.join(settings.BASE_DIR, 'docs/k8s_resource.csv')
        df = pd.read_csv(url, sep=',', engine='python')
        for index, row in df.iterrows():
            resource_name = row[0]
            short_name = row[1] if not pd.isnull(row[1]) else ""
            api_goup = row[2] if not pd.isnull(row[2]) else ""
            namespaced = row[3]
            resource_kind = row[4]

            KResource.objects.create(
                resource_name=resource_name,
                short_name=short_name,
                api_group=api_goup,
                namespaced=namespaced,
                kind=resource_kind,
            )
