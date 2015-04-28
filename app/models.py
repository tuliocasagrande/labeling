from django.db import models
from django.contrib.auth.models import User

class Dataset(models.Model):
  owner = models.ForeignKey(User)
  name = models.CharField(max_length=50)
  has_header = models.BooleanField(default=True)
  number_of_classes = models.IntegerField(default=2)
  class_column = models.CharField(max_length=50)

class Sample(models.Model):
  dataset = models.ForeignKey(Dataset)
  data = models.TextField()

class Label(models.Model):
  sample = models.ForeignKey(Sample)
  owner = models.ForeignKey(User)
  label = models.SmallIntegerField()
