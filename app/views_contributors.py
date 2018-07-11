from django.http import HttpResponse, JsonResponse

from app.models import Contribution
from django.contrib.auth.models import User


def create(request, dataset_id):
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.POST['contributor'])
            Contribution(dataset_id=dataset_id, contributor=user).save()
            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse(status=400)


def destroy(request, dataset_id, contributor):
    if request.method == 'DELETE':
        try:
            user = User.objects.get(username=contributor)
            (Contribution.objects
             .get(dataset_id=dataset_id, contributor=user)
             .delete())
            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse(status=400)


def search(request, query):
    users = User.objects.filter(username__contains=query)
    array = [dict(value='{0}'.format(u.username)) for u in users]
    return JsonResponse(array, safe=False)
