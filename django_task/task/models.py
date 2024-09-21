from django.db import models


class Task(models.Model):
    tittle = models.CharField(max_length=100, blank=False, verbose_name="заголовок")
    description = models.TextField(blank=True, verbose_name="описание")
    completed = models.BooleanField(default=False, verbose_name="готово")

    def __str__(self):
        return self.tittle
