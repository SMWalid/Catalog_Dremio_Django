from django.db import models
import uuid
from datasets.models import PhysicalDataset, VirtualDataset  # Import PDS & VDS

# Dataset Lineage Table (Tracks Parent-Child Relationships)
class DatasetLineage(models.Model):
    parent = models.ForeignKey(
        PhysicalDataset, null=True, blank=True, on_delete=models.CASCADE, related_name='children_pds', to_field='hash'
    )
    child = models.ForeignKey(
        VirtualDataset, null=True, blank=True, on_delete=models.CASCADE, related_name='parents_vds', to_field='hash'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('parent', 'child')

