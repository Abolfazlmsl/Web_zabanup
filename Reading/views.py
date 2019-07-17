from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from . import models
# Create your views here.


def home(request):
    if request.user:
        username = request.user.username
        return render(request, 'home.html', context={'user': username, })
    else:
        return render(request, 'home.html')


def reading(request):
    if request.user.is_authenticated:
        passages = models.Passage.objects.all()

        query_g1 = request.GET.get("group1")
        query_g2 = request.GET.get("group2")
        if query_g1 and query_g2:
            # pass
            return render(request, 'Reading/Detail.html', {'group1': query_g1, 'group2': query_g2})

        context = {'passages': passages}
        return render(request, 'Reading/reading.html', context)
    else:
        return redirect('Reading:home')


def passage_body(request, passage_id):
    passage = get_object_or_404(models.Passage, pk=passage_id)
    return render(request, 'Reading/passages.html', {'passage': passage})


def submit(request, passage_id):
    if request.method == 'POST':
        answer_list = []
        answer_text = []
        passage = get_object_or_404(models.Passage, pk=passage_id)

        q1 = request.POST.get('q1')
        answer_list.append(q1)
        q2 = request.POST.get('q2')
        answer_list.append(q2)
        q3 = request.POST.get('q3')
        answer_list.append(q3)
        q7 = request.POST.get('q7')
        answer_list.append(q7)
        q8 = request.POST.get('q8')
        answer_list.append(q8)
        q9 = request.POST.get('q9')
        answer_list.append(q9)

        hidden1 = request.POST.get('hidden1')
        hidden2 = request.POST.get('hidden2')
        hidden3 = request.POST.get('hidden3')
        q4 = request.POST.get('q4')
        q5 = request.POST.get('q5')
        q6 = request.POST.get('q6')
        answer_text.append([hidden1, q4])
        answer_text.append([hidden2, q5])
        answer_text.append([hidden3, q6])

        q10 = request.POST.getlist('q10')
        q10_id = request.POST.get('q10_id')

        grade = 0
        for answer in answer_list:
            my_answer = models.Answer.objects.get(id=answer).truth
            if my_answer:
                grade += 1

        for answer in answer_text:
            my_question = models.Question.objects.get(id=answer[0])
            if answer[1] == models.Answer.objects.get(question=my_question).text:
                grade += 1

        count_q10 = 0
        answers_10 = models.Answer.objects.filter(question=q10_id)
        for answer in answers_10:
            if answer.truth:
                count_q10 += 1
        for answer in q10:
            if models.Answer.objects.get(id=answer).truth:
                count_q10 -= 1
        if count_q10 == 0:
            grade += 1
        context = {
            'List': answer_list,
            'passage': passage,
            'grade': grade*10,
        }
        return render(request, 'Reading/submit.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('http://127.0.0.1:8000/')
        else:
            return render(request, 'login.html', context={'alert': 'The information is wrong!', })
    else:
        return render(request, 'login.html', context={})


def logout_view(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/')


def change_password(request):
    if request.method == 'POST':
        u = User.objects.get(username=request.user.username)
        newpass = request.POST['newpass']
        u.set_password(newpass)
        u.save()
        return redirect('http://127.0.0.1:8000/')
    else:
        return render(request, 'change_password.html')
