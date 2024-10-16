# models.py
from django.db import models

class Record(models.Model):
    in_count = models.IntegerField()  # Field for "In" value
    out_count = models.IntegerField()  # Field for "Out" value
    timestamp = models.DateTimeField()  # Field for "Time" value

    def __str__(self):
        return f"Record(In={self.in_count}, Out={self.out_count}, Time={self.timestamp})"