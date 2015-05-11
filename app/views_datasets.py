import csv
from cStringIO import StringIO
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import PermissionDenied

from app.models import Dataset, Sample, Label, Contribution

# GET /datasets/new
@login_required
def new(request):
  if request.method == 'GET':
    return render(request, 'app/datasets/new.html')

# POST /datasets/create
@login_required
def create(request):
  if request.method == 'POST':
    dataset = Dataset()
    dataset.owner = request.user
    dataset.name = request.POST['name']
    dataset.number_of_labels = request.POST['number_of_labels']

    if not dataset.privacy_validation(request.POST['privacy']):
      return render(request, '400.html', status=400)

    has_header = request.POST.get('has_header', False)
    dataset_file = request.FILES['dataset']
    reader = csv.reader(dataset_file)
    if has_header:
      dataset.label_name = request.POST['label_name']
      header_list = next(reader)
      label_index = header_list.index(dataset.label_name)
      header_list.pop(label_index)

      dataset.header = _write_row(header_list).strip()

    dataset.save()

    for row_list in reader:
      if has_header:
        label_string = row_list.pop(label_index)
        row = _write_row(row_list).strip()

        sample = Sample(dataset=dataset, data=row)
        sample.save()

        if label_string:
          label = Label(owner=request.user, sample=sample, label=label_string)
          label.save()

      else:
        row = _write_row(row_list).strip()
        sample = Sample(dataset=dataset, data=row)
        sample.save()

    return HttpResponseRedirect(reverse('datasets_show', args=(dataset.id,)))

# GET /datasets/<dataset_id>
def show(request, dataset_id):
  if request.method == 'GET':
    dataset = get_object_or_404(Dataset, pk=dataset_id)

    if not dataset.is_accessible_to(request.user):
      raise PermissionDenied

    user_is_owner = dataset.is_owned_by(request.user)
    if user_is_owner:
      contributors = Contribution.objects.filter(dataset=dataset, active=True)
    else:
      contributors = []

    context = {'dataset': dataset, 'contributors': contributors,
               'user_is_owner': user_is_owner}
    return render(request, 'app/datasets/show.html', context)

# DELETE /datasets/<dataset_id>/destroy
@login_required
def destroy(request, dataset_id):
  if request.method == 'DELETE':
    try:
      dataset = Dataset.objects.get(pk=dataset_id)
      if not dataset.is_owned_by(request.user):
        raise PermissionDenied

      dataset.delete()
      return JsonResponse(dict(redirect=reverse('index')))
    except Exception, e:
      raise e
      return HttpResponse(status=400)

# GET /datasets/<dataset_id>/download
def download(request, dataset_id):
  dataset = get_object_or_404(Dataset, pk=dataset_id)

  if not dataset.is_accessible_to(request.user):
    raise PermissionDenied

  samples = Sample.objects.filter(dataset=dataset)
  csv = u'{0},"{1}"\n'.format(dataset.header, dataset.label_name)
  print '{0} samples!!!'.format(len(samples))
  for sample in samples:
    labels = Label.objects.filter(sample=sample) #TODO: add active contributors
    if labels:
      label_list = [l.label for l in labels]

      # Finding the mode
      label = max(set(label_list), key=label_list.count)
    else:
      label = ''
    csv += u'{0},{1}\n'.format(sample.data, label)

  response = HttpResponse(csv, content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename="{0}.csv"'.format(dataset.name)
  return response

def _write_row(row_list):
  output = StringIO()
  csv.writer(output, quoting=csv.QUOTE_ALL).writerow(row_list)
  value = output.getvalue()
  output.close()
  return value
