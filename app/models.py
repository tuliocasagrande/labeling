from django.db import models
from django.contrib.auth.models import User

class Dataset(models.Model):
  owner = models.ForeignKey(User)

class Sample(models.Model):
  dataset = models.ForeignKey(Dataset)
  data = models.TextField()
  number_of_classes = models.IntegerField(default=2)

class Label(models.Model):
  sample = models.ForeignKey(Sample)
  label = models.SmallIntegerField()
  owner = models.ForeignKey(User)
