from django.db import models
from django.contrib.auth.models import User


class Dataset(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    privacy = models.CharField(default='restricted', max_length=10)
    number_of_labels = models.IntegerField(default=2)
    number_of_samples = models.IntegerField(default=0)
    header = models.TextField()

    def __unicode__(self):
        return self.name

    def is_owned_by(self, user):
        return self.owner == user

    def is_active_contributor(self, user):
        if Contribution.objects.filter(dataset=self,
                                       contributor=user.id,
                                       active=True):
            return True
        # Just to make sure it propagates a boolean and not an empty QuerySet
        return False

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
        return (self.is_owned_by(user) or
                self.privacy in ['public', 'restricted'] or
                self.is_active_contributor(user))

    def is_writable_by(self, user):
        return (self.is_owned_by(user) or
                self.privacy == 'public' or
                self.is_active_contributor(user))


class Contribution(models.Model):
    dataset = models.ForeignKey(Dataset)
    contributor = models.ForeignKey(User)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('dataset', 'contributor')


class Sample(models.Model):
    dataset = models.ForeignKey(Dataset)
    data = models.TextField()
    # just to create the CSV file in the same order
    original_index = models.IntegerField()
    times_labeled = models.IntegerField(default=0)


class Label(models.Model):
    sample = models.ForeignKey(Sample)
    owner = models.ForeignKey(User)
    label = models.SmallIntegerField()

    class Meta:
        unique_together = ('sample', 'owner')
