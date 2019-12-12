from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import random
from Reading import models


# Create your views here.


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.groups.filter(name='Manager').exists() or user.is_superuser:
                login(request, user)
                return redirect('manager:IndexView')
            else:
                return render(request, 'manager/login.html', context={'alert': 'You are not superuser or staff!!!', })
        else:
            return render(request, 'manager/login.html', context={'alert': 'The information is wrong!', })
    return render(request, 'manager/login.html')


def index(request):
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
        return render(request, 'manager/index.html')
    return redirect('manager:LoginView')


def logout_view(request):
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
        logout(request)
    return redirect('manager:LoginView')


def user_answer_list(request):
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
        all_user_answers = models.UserAnswer.objects.all().order_by('-time')
        alert = ''
        if request.POST.get('exam_id'):
            if all_user_answers.filter(exam_id=request.POST.get('exam_id')).exists():
                all_user_answers = all_user_answers.filter(exam_id=request.POST.get('exam_id'))
            else:
                alert += 'The exam does not exists!!! \n'
        if request.POST.get('student'):
            if all_user_answers.filter(user__username=request.POST.get('student')).exists():
                all_user_answers = all_user_answers.filter(user__username=request.POST.get('student'))
            else:
                alert += 'The user does not exists!!!'
        context = {
            'all_user_answers': all_user_answers,
            'alert': alert,
        }
        return render(request, 'manager/user_answer.html', context=context)
    return redirect('manager:LoginView')


def user_list(request):
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
        all_user = User.objects.filter(groups__name='Student')
        alert = ''
        if request.POST.get('username'):
            if all_user.filter(username=request.POST.get('username')).exists():
                all_user = all_user.filter(username=request.POST.get('username'))
            else:
                alert = 'The user does not exists!!!'
        if request.POST.get('email'):
            if all_user.filter(email=request.POST.get('email')).exists():
                all_user = all_user.filter(email=request.POST.get('email'))
            else:
                alert = 'The user does not exists!!!'
        if request.POST.get('phone_number'):
            if all_user.filter(profile__phone_number=request.POST.get('phone_number')).exists():
                all_user = all_user.filter(profile__phone_number=request.POST.get('phone_number'))
            else:
                alert = 'The user does not exists!!!'
        context = {
            'all_user': all_user,
            'alert': alert,
        }
        return render(request, 'manager/user.html', context)
    return redirect('manager:LoginView')


def user_edit(request, pk):
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:

        if request.POST.get('delete_btn'):
            current_user = User.objects.get(id=pk)
            current_user.delete()
            return redirect('manager:UserList')

        elif request.POST.get('edit_user_btn'):
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')

            my_user = User.objects.get(id=pk)
            all_users = User.objects.exclude(id=pk)
            all_profiles = models.Profile.objects.exclude(user_id=pk)

            username_exists = all_users.filter(username=username).exists()
            email_exists = all_users.filter(email=email).exists()
            phone_number_exists = all_profiles.filter(phone_number=phone_number).exists()

            if username_exists or email_exists or phone_number_exists:
                alert = ''
                if username_exists:
                    alert += 'The username is already taken!! \n'
                if email_exists:
                    alert += 'The email is already taken!! \n'
                if phone_number_exists:
                    alert += 'The phone number is already taken!! \n'
                context = {
                    'user': my_user,
                    'alert': alert,
                }
                return render(request, 'manager/edit_user.html', context)

            my_user.username = username
            my_user.email = email
            my_user.first_name = first_name
            my_user.last_name = last_name

            my_user.save()

            my_profile = models.Profile.objects.get(user_id=pk)
            my_profile.phone_number = phone_number
            my_profile.address = address
            my_profile.save()

            return redirect('manager:UserList')
        else:
            user = User.objects.get(id=pk)
            context = {
                'user': user,
            }
            return render(request, 'manager/edit_user.html', context)
    return redirect('manager:LoginView')


def exam_list(request):
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
        all_exams = models.Exam.objects.all()
        alert = ''
        if request.POST.get('exam_filter_btn'):
            book = request.POST.get('book_filter')
            category = request.POST.get('category_filter')
            difficulty = request.POST.get('difficulty_filter')
            if book:
                if all_exams.filter(book=book).exists():
                    all_exams = all_exams.filter(book=book)
                else:
                    alert = 'The exam does not exists!!!'
            if category:
                if all_exams.filter(category=category).exists():
                    all_exams = all_exams.filter(category=category)
                else:
                    alert = 'The exam does not exists!!!'
            if difficulty:
                if all_exams.filter(difficulty=difficulty).exists():
                    all_exams = all_exams.filter(difficulty=difficulty)
                else:
                    alert = 'The exam does not exists!!!'
        context = {
            'all_exams': all_exams,
            'alert': alert,
        }
        return render(request, 'manager/exam_list.html', context)
    return redirect('manager:LoginView')


def exam_create(request):
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
        if request.method == 'POST':
            book = request.POST.get('book')
            category = request.POST.get('category')
            difficulty = request.POST.get('difficulty')
            image = request.POST.get('image')
            models.Exam.objects.create(book=book, difficulty=difficulty, category=category, image=image)
            return redirect('manager:ExamList')
        else:
            context = {
                'exam': models.Exam
            }
            return render(request, 'manager/exam_create.html', context)
    return redirect('manager:LoginView')


def exam_edit(request, pk):
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
        if request.GET.get('delete_btn'):
            current_exam = models.Exam.objects.get(id=pk)
            current_exam.delete()
            return redirect('manager:ExamList')

        elif request.POST.get('edit_exam_btn'):
            book = request.POST.get('book')
            category = request.POST.get('category')
            difficulty = request.POST.get('difficulty')
            image = None
            if request.FILES:
                image = request.FILES['image']

            current_exam = models.Exam.objects.get(id=pk)
            current_exam.book = book
            current_exam.category = category
            current_exam.difficulty = difficulty
            if image is not None:
                current_exam.image = image
            current_exam.save()

            return redirect('manager:ExamList')

        else:
            current_exam = models.Exam.objects.get(id=pk)
            context = {
                'current_exam': current_exam,
                'exam': models.Exam,
            }
            return render(request, 'manager/exam_detail.html', context)
    return redirect('manager:LoginView')


def user_detail(request, pk):
    current_user = User.objects.get(id=pk)
    current_profile = models.Profile.objects.get(user=current_user)
    user_answers = models.UserAnswer.objects.filter(user=current_user)
    context = {
        'current_user': current_user,
        'current_profile': current_profile,
        'user_answers': user_answers,
    }
    return render(request, 'manager/user_detail.html', context)


def send_ticket(request):
    if request.method == 'POST':
        all_user = User.objects.all()
        text = request.POST.get('text')
        title = request.POST.get('title')
        subject = request.POST.get('subject')
        receivers = []
        for user in all_user:
            if request.POST.get('receiver' + str(user.id)):
                receivers.append(request.POST.get('receiver' + str(user.id)))
        for receiver in receivers:
            user = User.objects.get(id=receiver)
            current_ticket = models.Ticket.objects.create(title=title,
                                                          relate_unit=subject,
                                                          staff=request.user,
                                                          student=user)
            models.TicketMessage.objects.create(ticket=current_ticket,
                                                sender=request.user,
                                                text=text)
        return redirect('manager:Ticket')
    all_user = User.objects.filter(is_superuser=False)
    context = {
        'all_user': all_user,
        'subjects': models.Ticket.CHOICES,
    }
    return render(request, 'manager/send_ticket.html', context)


def ticket(request):
    all_tickets = models.Ticket.objects.all()
    alert = ''
    if request.method == 'POST':
        username = request.POST.get('student')
        title = request.POST.get('title')
        if username:
            user_check = User.objects.filter(username=username)
            if user_check.exists():
                student = User.objects.get(username=username)
                if all_tickets.filter(student=student).exists():
                    all_tickets = all_tickets.filter(student=student)
            else:
                alert = 'The ticket does not exists!!!'
        if title:
            if all_tickets.filter(title=title).exists():
                all_tickets = all_tickets.filter(title=title)
            else:
                alert = 'The ticket does not exists!!!'
    context = {
        'alert': alert,
        'all_tickets': all_tickets,
    }
    return render(request, 'manager/ticket.html', context)


def ticket_history(request, pk):
    if request.method == 'POST':
        text = request.POST.get('new_message')
        models.TicketMessage.objects.update_or_create(ticket_id=pk, text=text, sender=request.user)
    messages_for_ticket = models.TicketMessage.objects.filter(ticket_id=pk)
    context = {
        'messages_for_ticket': messages_for_ticket,
    }
    return render(request, 'manager/ticket_history.html', context)
