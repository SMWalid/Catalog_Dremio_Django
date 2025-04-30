from django.core.management.base import BaseCommand
from datasets.jdbc_utils import fetch_paths_from_dremio
from datasets.models import VirtualDataset

class Command(BaseCommand):
    help = "Fetch Virtual Datasets (VDS) from Dremio and insert new ones into the database"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("🔄 Fetching VDS paths from Dremio..."))

        vds_list = fetch_paths_from_dremio('SELECT path FROM sys.views')

        # Get existing hashes from DB
        existing_hashes = set(VirtualDataset.objects.values_list('hash', flat=True))

        new_vds = []
        for item in vds_list:
            if item["hash"] not in existing_hashes:
                new_vds.append(VirtualDataset(
                    name=item["name"],
                    path=item["path"],
                    hash=item["hash"],
                    space=item["full_path_list"][0]  # First element is the space
                ))

        # Bulk insert new VDSs
        VirtualDataset.objects.bulk_create(new_vds)

        self.stdout.write(self.style.SUCCESS(f"✅ {len(new_vds)} new Virtual Datasets inserted."))
