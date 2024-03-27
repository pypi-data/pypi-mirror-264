from django.db import models


class Timestamp(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=512, unique=True)
    timestamp = models.BinaryField()

    def __str__(self):
        return self.name
