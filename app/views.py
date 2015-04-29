from django.http import HttpResponse
from django.shortcuts import render

from app.models import Dataset

# GET /
def index(request):
  q = Dataset.objects.filter(owner=request.user.id)
  print q

  return render(request, 'app/index.html', {})


# GET /dataset/new
# POST /dataset/new
def new_dataset(request):
  if request.method == 'POST':
    print request.POST['title']
    print request.POST['number_of_labels']
    print request.POST.get('has_header', False)
    print request.POST['label_column_name']
    dataset = request.FILES['dataset']
    s = ''
    if dataset:
      for line in dataset:
        s += line

    return HttpResponse(s)

  elif request.method == 'GET':
    return render(request, 'app/new_dataset.html', {})
