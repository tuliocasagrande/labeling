import unicodecsv as csv
from StringIO import StringIO
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import PermissionDenied
from django.template.loader import render_to_string

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
    dataset.description = request.POST['description']

    if not dataset.privacy_validation(request.POST['privacy']):
      return render(request, '400.html', status=400)

    dataset_file = request.FILES['dataset']
    reader = csv.reader(dataset_file, encoding='utf-8')
    header_list = reader.next()

    label_name = request.POST.get('label_name', 'CLASS')
    append_label_column = request.POST.get('append_label_column', False)
    if not append_label_column:
      label_index = header_list.index(label_name)
      header_list.pop(label_index)

    header_list.append(label_name)
    dataset.header = csvlist_to_string(header_list).strip()
    dataset.save()

    samples_count = 0
    for row_list in reader:
      samples_count += 1
      if not append_label_column:
        label_string = row_list.pop(label_index)

      row = csvlist_to_string(row_list).strip()
      sample = Sample(dataset=dataset, data=row, original_index=samples_count)
      sample.save()

      if not append_label_column and label_string:
        label = Label(owner=request.user, sample=sample, label=label_string)
        label.save()
        sample.times_labeled = 1
        sample.save()

    dataset.number_of_samples = samples_count
    dataset.save()

    return HttpResponseRedirect(reverse('datasets_show', args=(dataset.id,)))

# GET /datasets/<dataset_id>
def show(request, dataset_id):
  if request.method == 'GET':
    dataset = get_object_or_404(Dataset, pk=dataset_id)

    if dataset.is_owned_by(request.user):
      contributors = Contribution.objects.filter(dataset=dataset, active=True)
      context = {'dataset': dataset, 'contributors': contributors}
      return render(request, 'app/datasets/show_admin.html', context)

    else:
      if not dataset.is_readable_by(request.user):
        raise PermissionDenied

      context = {'dataset': dataset}
      return render(request, 'app/datasets/show.html', context)

# GET /photos/<dataset_id>/edit
@login_required
def edit(request, dataset_id):
  if request.method == 'GET':
    dataset = get_object_or_404(Dataset, pk=dataset_id)

    if not dataset.is_owned_by(request.user):
      raise PermissionDenied

    context = {'dataset': dataset}
    return render(request, 'app/datasets/edit.html', context)

# POST /photos/<dataset_id>/update
@login_required
def update(request, dataset_id):
  if request.method == 'POST':
    dataset = get_object_or_404(Dataset, pk=dataset_id)

    if not dataset.is_owned_by(request.user):
      raise PermissionDenied

    dataset.name = request.POST['name']
    dataset.number_of_labels = request.POST['number_of_labels']
    dataset.description = request.POST['description']
    if not dataset.privacy_validation(request.POST['privacy']):
      return render(request, '400.html', status=400)
    dataset.save()

    return HttpResponseRedirect(reverse('datasets_show', args=(dataset.id,)))

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

# GET /datasets/<dataset_id>/label
# POST /datasets/<dataset_id>/label
@login_required
def label(request, dataset_id):
  dataset = get_object_or_404(Dataset, pk=dataset_id)
  if not dataset.is_writable_by(request.user):
    raise PermissionDenied

  if request.method == 'GET':
    # user_labeled_samples = Label.objects.filter(owner=request.user, sample=sample).values('sample_id')
    # samples = Sample.objects.filter(dataset=dataset).order_by('times_labeled').exclude(pk__in=user_labeled_samples)

    samples = Sample.objects.filter(dataset=dataset).order_by('times_labeled')
    samples = samples[:10]

    dataset.header = string_to_csvlist(dataset.header)
    for s in samples:
      s.data = string_to_csvlist(s.data)

    context = {'dataset': dataset, 'samples': samples}

    if request.is_ajax():
      html = render_to_string('app/datasets/_sample_rows.html', context)
      return HttpResponse(html)
    else:
      return render(request, 'app/datasets/label.html', context)

  elif request.method == 'POST':
    sample = Sample.objects.get(pk=request.POST['sample_id'])

    obj, created = Label.objects.update_or_create(
                      owner=request.user, sample=sample,
                      defaults={'label': request.POST['label']})

    if created:
      sample.times_labeled += 1
      sample.save()

    return HttpResponse()

# GET /datasets/<dataset_id>/download
def download(request, dataset_id):
  dataset = get_object_or_404(Dataset, pk=dataset_id)

  if not dataset.is_readable_by(request.user):
    raise PermissionDenied

  samples = Sample.objects.filter(dataset=dataset).order_by('original_index')
  csv = u'{0}\n'.format(dataset.header)
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

def csvlist_to_string(csvlist):
  f = StringIO()
  csv.writer(f, quoting=csv.QUOTE_MINIMAL, encoding='utf-8').writerow(csvlist)
  string = f.getvalue()
  f.close()
  return string

def string_to_csvlist(string):
  f = StringIO(string.encode('utf8'))
  csvlist = csv.reader(f, encoding='utf-8').next()
  f.close()
  return csvlist
