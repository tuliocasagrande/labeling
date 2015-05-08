from django.db import models
from django.contrib.auth.models import User

class Dataset(models.Model):
  owner = models.ForeignKey(User)
  name = models.CharField(max_length=50)
  privacy = models.CharField(default='restricted', max_length=10)
  number_of_labels = models.IntegerField(default=2)
  header = models.TextField(null=True, blank=True)
  label_name = models.CharField(max_length=50, null=True, blank=True)

  def __unicode__(self):
    return self.name

  def privacy_validation(self, privacy):
    if privacy in ['public', 'restricted', 'private']:
      self.privacy = privacy
      return True
    return False

  def is_accessible_to(self, user):
    if self.is_owned_by(user) or self.privacy in ['public', 'restricted']:
      return True

    contributors = Contribution.objects.filter(dataset=self, active=True)
    if user in [c.contributor for c in contributors]:
      return True

    return False

  def is_owned_by(self, user):
    return True if self.owner == user else False

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
