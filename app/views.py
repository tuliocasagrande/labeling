from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from app.models import Contribution, Dataset
from django.contrib.auth.models import User

# GET /
def index(request):
  if request.user.is_authenticated():
    my_datasets = Dataset.objects.filter(owner=request.user.id)
    others_datasets = Contribution.objects.filter(contributor=request.user.id)
    public_datasets = Dataset.objects.filter(privacy='public')

    context = {'my_datasets': my_datasets, 'others_datasets': others_datasets,
               'public_datasets': public_datasets}
    return render(request, 'app/dashboard.html', context)
  else:
    return render(request, 'app/index.html')

# GET /accounts/profile
@login_required
def accounts_profile(request):
  return render(request, 'app/accounts_profile.html', {})
