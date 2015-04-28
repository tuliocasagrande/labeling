from django.http import HttpResponse
from django.shortcuts import render

from app.models import Dataset

def index(request):
  q = Dataset.objects.filter(owner=request.user.id)
  print q

  return render(request, 'app/index.html', {})




def new_dataset(request):
  if request.method == 'POST':
      dataset = request.FILES['dataset']
      s = ''
      if dataset:
        for line in dataset:
          s += line

      return HttpResponse(s)
  else:
    return render(request, 'app/index.html', {})
