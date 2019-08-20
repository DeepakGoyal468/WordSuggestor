from django.db import models

# Create your models here
class Query(models.Model):
    word_name = models.CharField(max_length=100)
    word_frequency = models.IntegerField()
    word_length = models.IntegerField(default=0)

    def __str__(self):
        return self.word_name
