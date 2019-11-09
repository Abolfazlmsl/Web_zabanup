from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect
from Reading import models

# Create your views here.


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.groups.filter(name='Manager').exists() or User.objects.get(username=username).is_superuser:
                login(request, user)
                return redirect('manager:IndexView')
            else:
                return render(request, 'manager/login.html', context={'alert': 'You are not superuser or staff!!!', })
        else:
            return render(request, 'manager/login.html', context={'alert': 'The information is wrong!', })
    return render(request, 'manager/login.html')


def index(request):
    if request.user.is_authenticated:
        return render(request, 'manager/index.html')
    return redirect('manager:LoginView')


def logout_view(request):
    logout(request)
    return redirect('manager:LoginView')


def exam_list(request):
    all_user_answers = models.UserAnswer.objects.all().order_by('-time')
    alert = ''
    if request.POST.get('exam_id'):
        if all_user_answers.filter(exam_id=request.POST.get('exam_id')).exists():
            all_user_answers = all_user_answers.filter(exam_id=request.POST.get('exam_id'))
        else:
            alert += 'The exam does not exists!!!'
    if request.POST.get('student'):
        if all_user_answers.filter(user__username=request.POST.get('student')).exists():
            all_user_answers = all_user_answers.filter(user__username=request.POST.get('student'))
        else:
            alert += '\n The user does not exists!!!'
    context = {
        'all_user_answers': all_user_answers,
        'alert': alert,
    }
    return render(request, 'manager/exam.html', context=context)
