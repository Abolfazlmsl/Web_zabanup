from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.shortcuts import render
from Reading import models
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.contrib.auth.decorators import login_required


# view for editing information of user
@login_required(login_url="/student/login/")
def edit_information(request):
    if request.method == 'POST':
        current_user = request.user
        new_user_name = request.POST.get("new_user_name")
        new_first_name = request.POST.get("new_first_name")
        new_last_name = request.POST.get("new_last_name")
        new_email = request.POST.get("new_email")
        new_phone = request.POST.get("new_phone")
        new_address = request.POST.get("new_address")

        all_users = User.objects.exclude(id=request.user.id)
        all_profiles = models.Profile.objects.exclude(user_id=request.user.id)

        username_exists = all_users.filter(username=new_user_name).exists()
        email_exists = all_users.filter(email=new_email).exists()
        phone_number_exists = all_profiles.filter(phone_number=new_phone).exists()

        # check that new user name or email or address exists or not
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
            current_user.first_name = new_first_name
            current_user.last_name = new_last_name
            current_user.email = new_email
            current_user.save()

            models.Profile.objects.update(user=current_user, phone_number=new_phone, address=new_address)

            context = {
                'success': 'your information updated successfully!'
            }
            return render(request, 'student/edit_information.html', context)
    else:
        return render(request, 'student/edit_information.html')


# view for editing password of user
@login_required(login_url="/student/login/")
def change_password(request):
    if request.method == 'POST':
        current_user = User.objects.get(id=request.user.id)
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        re_new_password = request.POST.get("re_new_password")

        if not check_password(current_password, current_user.password):
            context = {
                'wrong_password_alert': 'Your current password is wrong!'
            }
            return render(request, 'student/change_password.html', context)
        elif new_password != re_new_password:
            context = {
                'not_match_alert': 'Passwords does not match!',
            }
            return render(request, 'student/change_password.html', context)

        else:
            current_user.set_password(new_password)
            current_user.save()
            logout(request)
            return redirect('student:UserLogin')
    else:
        return render(request, 'student/change_password.html')


# view for student login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('student:index')
        else:
            return render(request, 'student/login.html',
                          context={'alert': 'user with this information does not exists!'})
    else:
        return render(request, 'student/login.html')


# view for index of student panel
@login_required(login_url="/student/login/")
def panel(request):
    return render(request, 'student/index.html')


# view for compare user grades with others and him/herself
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


# view for compare user grades with others and him/herself in a specific exam
@login_required(login_url="/student/login/")
def exam_answer_detail(request, pk):
    user_answer = models.UserAnswer.objects.filter(user=request.user, exam_id=pk).order_by('-grade')[:10]
    user_answer_by_time = models.UserAnswer.objects.filter(user=request.user, exam_id=pk)
    all_answer = models.UserAnswer.objects.filter(exam_id=pk).order_by('-grade')[:10]
    my_comment = models.Comment.objects.filter(user=request.user, exam_id=pk).order_by('-time')

    # show and delete user comments
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
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


# view for showing tickets of user
@login_required(login_url="/student/login/")
def tickets(request):
    user_message = models.Ticket.objects.filter(student=request.user).order_by('date')

    context = {
        'user_message': user_message
    }

    return render(request, 'student/tickets.html', context)


# view for sending ticket to staff
def send_tickets(request):
    all_manager = User.objects.filter(groups__name='Manager')
    if request.method == 'POST':
        ticket_title = request.POST.get('ticket_title')
        message_text = request.POST.get('message_text')
        related_unit = request.POST.get('related_unit')

        chosen_persons = []

        for user in all_manager:
            checkbox_id = 'user' + str(user.id)
            manager = request.POST.get(checkbox_id)
            if manager:
                chosen_persons.append(manager)

        for person in chosen_persons:
            person_user = User.objects.get(id=person)
            current_ticket = models.Ticket.objects.update_or_create(title=ticket_title, relate_unit=related_unit,
                                                                    student=request.user, staff=person_user)
            models.TicketMessage.objects.update_or_create(ticket=current_ticket[0], sender=request.user,
                                                          text=message_text)

    all_tickets = models.Ticket.objects.filter(student=request.user)
    choices_of_ticket = models.Ticket.CHOICES
    context = {
        'all_manager': all_manager,
        'all_tickets': all_tickets,
        'choices_of_ticket': choices_of_ticket,
    }

    return render(request, 'student/send_ticket.html', context)


# view for specific ticket and send message in that ticket
def ticket_chat(request, pk):
    if request.method == 'POST':
        message_text = request.POST.get('message_text')

        models.TicketMessage.objects.update_or_create(ticket_id=pk, sender=request.user, text=message_text)

    all_messages = models.TicketMessage.objects.filter(ticket_id=pk).order_by('time')
    context = {
        'all_messages': all_messages
    }
    return render(request, 'student/ticket_chat.html', context=context)


# view for start chatting with a user
def user_chat(request):
    sender_user = request.user
    receiver = User.objects.filter(groups__name='Student').exclude(id=sender_user.id)
    if request.method == 'POST':
        text = request.POST.get('message_text')
        receiver_list = []
        for user in receiver:
            user_id = 'user' + str(user.id)
            chosen_user = request.POST.get(user_id)
            if chosen_user:
                receiver_list.append(chosen_user)

        for user in receiver_list:
            person_user = User.objects.get(id=user)
            current_chat = models.Chat.objects.update_or_create(sender=sender_user, receiver=person_user)
            models.ChatMessage.objects.update_or_create(chat=current_chat[0], text=text, sender=sender_user)

    all_chats = models.Chat.objects.filter(sender=request.user) or models.Chat.objects.filter(receiver=request.user)
    context = {
        'all_chats': all_chats,
        'all_user': receiver,
    }

    return render(request, 'student/send_chat.html', context=context)


# view for chat page with a specific user
def chat(request, pk):
    if request.method == 'POST':
        message_text = request.POST.get('message_text')

        models.ChatMessage.objects.update_or_create(chat_id=pk, sender=request.user, text=message_text)
    all_messages = models.ChatMessage.objects.filter(chat_id=pk).order_by('time')
    context = {
        'all_messages': all_messages
    }
    return render(request, 'student/chat.html', context=context)


def student_panel_view(request):
    return render(request, 'student/student-panel.html')


def exams_history_view(request):
    return render(request, 'student/student-panel-exam.html')