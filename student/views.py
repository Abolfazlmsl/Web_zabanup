from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.shortcuts import render
from Reading import models
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.contrib.auth.decorators import login_required


# Create your views here.


@login_required(login_url="/student/login/")
def edit_information(request):
    if request.method == 'POST':
        u = User.objects.get(id=request.user.id)
        newuser = request.POST.get('newuser')
        new_firstname = request.POST.get('new_firstname')
        new_lastname = request.POST.get('new_lastname')
        new_email = request.POST.get('new_email')
        new_phone = request.POST.get('new_phone')
        new_address = request.POST.get('new_address')

        all_users = User.objects.exclude(id=request.user.id)
        all_profiles = models.Profile.objects.exclude(user_id=request.user.id)

        username_exists = all_users.filter(username=newuser).exists()
        email_exists = all_users.filter(email=new_email).exists()
        phone_number_exists = all_profiles.filter(phone_number=new_phone).exists()

        if username_exists or email_exists or phone_number_exists:
            alert = ''
            if username_exists:
                alert += 'this username is already taken \n'
            if email_exists:
                alert += 'this email is already taken \n'
            if phone_number_exists:
                alert += 'this phone number is already taken \n'
            context = {
                'conflict_alert': alert
            }
            return render(request, 'student/edit_information.html', context)

        else:
            u.first_name = new_firstname
            u.last_name = new_lastname
            u.email = new_email
            u.save()

            prof = models.Profile.objects.update(user=u, phone_number=new_phone, address=new_address)

            context = {
                'success': 'your information updated successfully!'
            }
            return render(request, 'student/edit_information.html', context)
    else:
        return render(request, 'student/edit_information.html')


@login_required(login_url="/student/login/")
def change_password(request):
    if request.method == 'POST':
        u = User.objects.get(id=request.user.id)
        pswd = request.POST.get('pswd')
        newpass = request.POST.get('newpass')
        re_newpass = request.POST.get('re_newpass')

        if not check_password(pswd, u.password):
            context = {
                'alerrrt': 'Your current password is wrong!'
            }
            return render(request, 'student/change_password.html', context)
        elif newpass != re_newpass:
            context = {
                'alert': 'Passwords does not match!',
            }
            return render(request, 'student/change_password.html', context)

        else:
            u.set_password(newpass)
            u.save()
            logout(request)
            return redirect('student:UserLogin')
    else:
        return render(request, 'student/change_password.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('student:index')
        else:
            return render(request, 'student/login.html', context={'alert': 'user with this information does not exists!'})
    else:
        return render(request, 'student/login.html')


@login_required(login_url="/student/login/")
def panel(request):
    return render(request, 'student/index.html')


@login_required(login_url="/student/login/")
def answers(request):
    my_answers = models.UserAnswer.objects.filter(user=request.user).order_by('-grade')[:10]
    other_answers = models.UserAnswer.objects.exclude(user=request.user).order_by('-grade')[:10]
    exams = models.Exam.objects.all()

    context = {
        'my_answers': my_answers,
        'other_answers': other_answers,
        'exams': exams,
    }
    return render(request, 'student/exam.html', context)


@login_required(login_url="/student/login/")
def exam_answer_detail(request, pk):
    user_answer = models.UserAnswer.objects.filter(user=request.user, exam_id=pk).order_by('-grade')[:10]
    user_answer_by_time = models.UserAnswer.objects.filter(user=request.user, exam_id=pk)
    all_answer = models.UserAnswer.objects.filter(exam_id=pk).order_by('-grade')[:10]
    my_comment = models.Comment.objects.filter(user=request.user, exam_id=pk).order_by('-time')
    # passages_of_exam = models.UserAnswer.objects.filter(exam_id=pk, user=request.user).question_set.all()
    # print(passages_of_exam)
    if request.method == 'POST':
        comment_id = request.POST.get('cmnt_id')
        obj = models.Comment.objects.get(id=comment_id)
        obj.delete()
    if not my_comment:
        context = {
            'user_answer': user_answer,
            'all_answer': all_answer,
            'no_comment': 'There is no comment',
        }
        return render(request, 'student/exam_detail.html', context)
    else:
            context = {
                'user_answer': user_answer,
                'all_answer': all_answer,
                'my_comment': my_comment,
            }

            return render(request, 'student/exam_detail.html', context)


@login_required(login_url="/student/login/")
def messages(request):
    user_message = models.Message.objects.filter(receiver=request.user).order_by('time')

    context = {
        'user_message': user_message
    }

    return render(request, 'student/messages.html', context)


def send_messages(request):
    all_user = User.objects.exclude(id=request.user.id)
    if request.method == 'POST':
        message_title = request.POST.get('message_title')
        message_text = request.POST.get('message_text')

        choosed_persons = []

        for user in all_user:
            checkbox_id = 'user'+str(user.id)
            receiver = request.POST.get(checkbox_id)
            if receiver:
                choosed_persons.append(receiver)

        for person in choosed_persons:
            person_user = User.objects.get(id=person)
            models.Message.objects.update_or_create(sender=request.user, receiver=person_user, title=message_title,
                                                    text=message_text)

    all_messages = models.Message.objects.filter(sender=request.user)
    context = {
        'all_user': all_user,
        'all_messages': all_messages
    }

    return render(request, 'student/sent_message.html', context)

