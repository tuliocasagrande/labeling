from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from app.models import Dataset
from django.contrib.auth.models import User

# GET /
def index(request):
  if request.user.is_authenticated():
    query = Dataset.objects.filter(owner=request.user.id)
    print '{0} datasets!!!'.format(len(query))
    query.delete()

    return render(request, 'app/dashboard.html')
  else:
    return render(request, 'app/index.html')

# GET /accounts/profile
@login_required
def accounts_profile(request):
  return render(request, 'app/accounts_profile.html', {})
