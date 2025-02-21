from django.db import models

from users.models import User



class Parking(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing ID (optional, Django does this by default)
    name = models.CharField(max_length=255)  # Name of the parking
    schema = models.CharField(max_length=255)  # Stores the parking layout as a string
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to the user who created it
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically stores creation time

    def __str__(self):
        return self.name

