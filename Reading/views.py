from django.contrib.auth import authenticate, login
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from . import models
# Create your views here.


def home(request):
    return render(request, 'home.html')


def reading(request):
    passages = models.Passage.objects.all()
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


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        print(request.user)
        if user:
            login(request, user)
            return redirect('http://127.0.0.1:8000/')
        else:
            return render(request, 'login.html', context={})
    else:
        return render(request, 'login.html', context={})
