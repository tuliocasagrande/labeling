from django.db import models
from django.contrib.auth.models import User

class Dataset(models.Model):
  owner = models.ForeignKey(User)
  title = models.CharField(max_length=50)
  privacy = models.CharField(default='restricted', max_length=10)
  number_of_labels = models.IntegerField(default=2)
  header = models.TextField(null=True, blank=True)
  label_name = models.CharField(max_length=50, null=True, blank=True)

  def __unicode__(self):
    return self.title

  def privacy_validation(self, privacy):
    if privacy in ['public', 'restricted', 'private']:
      self.privacy = privacy
      return True
    return False

  def is_accessible(self, user):
    if self.owner == user or self.privacy in ['public', 'restricted']:
      return True

    contributors = Contribution.objects.filter(dataset=self, active=True)
    if user in [c.contributor for c in contributors]:
      return True

class Contribution(models.Model):
  dataset = models.ForeignKey(Dataset)
  contributor = models.ForeignKey(User)
  active = models.BooleanField(default=True)

class Sample(models.Model):
  dataset = models.ForeignKey(Dataset)
  data = models.TextField()

class Label(models.Model):
  sample = models.ForeignKey(Sample)
  owner = models.ForeignKey(User)
  label = models.SmallIntegerField()
