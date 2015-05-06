import csv
from cStringIO import StringIO
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from app.models import Dataset, Sample, Label
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

# GET /datasets/new
# POST /datasets/new
@login_required
def datasets_new(request):
  if request.method == 'POST':
    dataset = Dataset()
    dataset.owner = request.user
    dataset.title = request.POST['title']
    dataset.number_of_labels = request.POST['number_of_labels']
    dataset.privacy = request.POST['privacy']

    if dataset.privacy not in ['public', 'restricted', 'private']:
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

    legacy_labels_owner = User.objects.get(username='legacy_labels_owner')
    for row_list in reader:
      if has_header:
        label_string = row_list.pop(label_index)
        row = _write_row(row_list).strip()

        sample = Sample(dataset=dataset, data=row)
        sample.save()

        if label_string:
          label = Label(owner=legacy_labels_owner, sample=sample, label=label_string)
          label.save()

      else:
        row = _write_row(row_list).strip()
        sample = Sample(dataset=dataset, data=row)
        sample.save()

    return HttpResponseRedirect(reverse('datasets_show', args=(dataset.id,)))

  elif request.method == 'GET':
    return render(request, 'app/datasets_new.html')

# GET /datasets/<datasets_id>
def datasets_show(request, datasets_id):
  return HttpResponse(datasets_id);

# GET /datasets/<datasets_id>/download
def datasets_download(request, datasets_id):
  dataset = get_object_or_404(Dataset, pk=datasets_id)

  # TODO: privacy
  # if datataset.privacy == 'private':
  #  contributors = Contributor.objects.filter...
  #    if request.user not int contributors...
  #      raise forbidden

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
  response['Content-Disposition'] = 'attachment; filename="{0}.csv"'.format(dataset.title)
  return response

# GET /accounts/profile
@login_required
def accounts_profile(request):
  return render(request, 'app/accounts_profile.html', {})

def _write_row(row_list):
  output = StringIO()
  csv.writer(output, quoting=csv.QUOTE_ALL).writerow(row_list)
  value = output.getvalue()
  output.close()
  return value
