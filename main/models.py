from django.db import models

class Barcode(models.Model):
    value = models.CharField(max_length=100, unique=True)
    status = models.BooleanField(default=False)  # False = bajarilmagan, True = bajarilgan
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.value