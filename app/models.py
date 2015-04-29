from django.db import models
from django.contrib.auth.models import User

class Dataset(models.Model):
  owner = models.ForeignKey(User)
  title = models.CharField(max_length=50)
  header = models.TextField(null=True, blank=True)
  number_of_labels = models.IntegerField(default=2)
  label_column_name = models.CharField(max_length=50)

class Sample(models.Model):
  dataset = models.ForeignKey(Dataset)
  data = models.TextField()

class Label(models.Model):
  sample = models.ForeignKey(Sample)
  owner = models.ForeignKey(User)
  label = models.SmallIntegerField()
