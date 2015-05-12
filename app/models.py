from django.db import models
from django.contrib.auth.models import User

class Dataset(models.Model):
  owner = models.ForeignKey(User)
  name = models.CharField(max_length=50)
  description = models.TextField(null=True, blank=True)
  privacy = models.CharField(default='restricted', max_length=10)
  number_of_labels = models.IntegerField(default=2)
  number_of_samples = models.IntegerField(default=0)
  header = models.TextField(null=True, blank=True)
  label_name = models.CharField(max_length=50, null=True, blank=True)

  def __unicode__(self):
    return self.name

  def is_owned_by(self, user):
    return self.owner == user

  """ Privacy options
  Public      Anyone can read and write
  Restricted  Anyone can read. Only contributors can write
  Private     Only contributors can read and write
  """

  def privacy_validation(self, privacy):
    if privacy in ['public', 'restricted', 'private']:
      self.privacy = privacy
      return True
    return False

  def is_readable_by(self, user):
    if (self.is_owned_by(user) or
        self.privacy in ['public', 'restricted'] or
        Contribution.objects.filter(dataset=self, contributor=user.id, active=True)):
      # Just to make sure this method does not return the [] from the QuerySet
      return True
    return False

  def is_writable_by(self, user):
    if (self.is_owned_by(user) or
        self.privacy == 'public' or
        Contribution.objects.filter(dataset=self, contributor=user.id, active=True)):
      # Just to make sure this method does not return the [] from the QuerySet
      return True
    return False


class Contribution(models.Model):
  dataset = models.ForeignKey(Dataset)
  contributor = models.ForeignKey(User)
  active = models.BooleanField(default=True)

  class Meta:
    unique_together = ('dataset', 'contributor')


class Sample(models.Model):
  dataset = models.ForeignKey(Dataset)
  data = models.TextField()
  original_index = models.IntegerField()  # just to create the CSV file in the same order
  times_labeled = models.IntegerField(default=0)


class Label(models.Model):
  sample = models.ForeignKey(Sample)
  owner = models.ForeignKey(User)
  label = models.SmallIntegerField()

  class Meta:
    unique_together = ('sample', 'owner')
