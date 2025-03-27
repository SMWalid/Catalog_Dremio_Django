from django.db import models
import hashlib

# Function to generate a unique hash from the dataset path
def generate_hash(path):
    return hashlib.sha256(path.encode()).hexdigest()

# Physical Dataset (PDS)
class PhysicalDataset(models.Model):
    hash = models.CharField(max_length=64, primary_key=True, unique=True, editable=False, blank=True) # Efficient index key
    path = models.CharField(max_length=512, unique=True, blank=True)
    name = models.CharField(max_length=255)
    source = models.CharField(max_length=255)  # Represents the source of the PDS
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.hash:  # Only generate hash if it's empty
            self.hash = generate_hash(self.path)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Virtual Dataset (VDS)
class VirtualDataset(models.Model):
    hash = models.CharField(max_length=64, primary_key=True, unique=True, editable=False, blank=True)  # Efficient index key
    path = models.CharField(max_length=512, unique=True, blank=True)
    name = models.CharField(max_length=255)
    space = models.CharField(max_length=255)  # Represents the space of the VDS
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.hash:  # Only generate hash if it's empty
            self.hash = generate_hash(self.path)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
