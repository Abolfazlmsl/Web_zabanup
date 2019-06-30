from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from . import models
# Create your views here.


def home(request):
    return render(request, 'home.html')


def reading(request):
    passages = models.Passage.objects.all()

    query_g1 = request.GET.get("group1")
    query_g2 = request.GET.get("group2")
    if query_g1 and query_g2:
        # pass
        return render(request, 'Reading/Detail.html', {'group1': query_g1, 'group2': query_g2})

    context = {'passages': passages}
    return render(request, 'Reading/reading.html', context)


def passage_body(request, passage_id):
    passage = get_object_or_404(models.Passage, pk=passage_id)
    return render(request, 'Reading/passages.html', {'passage': passage})


def submit(request, passage_id):
    # if request.method == 'POST':
    passage = get_object_or_404(models.Passage, pk=passage_id)
    if request.method == 'POST':
        answer_list = request.POST.getlist('answer')
        # answer_list = passage.question_set.get(pk=request.POST.getlist('question.id'))
    context = {
        'List': answer_list,
        'passage': passage,
    }
    return render(request, 'Reading/submit.html', context)

