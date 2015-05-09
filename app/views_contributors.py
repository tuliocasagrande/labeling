from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse

from app.models import Dataset, Contribution
from django.contrib.auth.models import User

def create(request, dataset_id):
  if request.method == 'POST':
    try:
      dataset = Dataset.objects.get(pk=dataset_id)
      user = User.objects.get(username=request.POST['contributor'])
      Contribution(dataset=dataset, contributor=user).save()
      return HttpResponse(status=200)
    except Exception, e:
      return HttpResponse(status=400)

def destroy(request, dataset_id, contributor):
  if request.method == 'DELETE':
    try:
      dataset = Dataset.objects.get(pk=dataset_id)
      user = User.objects.get(username=contributor)
      Contribution.objects.get(dataset=dataset, contributor=user).delete()
      return HttpResponse(status=200)
    except Exception, e:
      return HttpResponse(status=400)

def search(request, query):
  users = User.objects.filter(username__contains=query)
  array = [dict(value='{0}'.format(u.username)) for u in users]
  return JsonResponse(array, safe=False)

