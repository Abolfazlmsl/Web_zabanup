from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from Reading import models


# Create your views here.


# home page for manager plan
def index(request):
    # check the login user is staff or superuser
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
        return render(request, 'manager/index.html')
    return redirect('manager:LoginView')


# this view for login staff or superuser to manager panel
def login_view(request):
    if request.method == 'POST':
        # get username and password from client
        username = request.POST.get('username')
        password = request.POST.get('password')
        # authenticate user
        user = authenticate(request, username=username, password=password)
        # check if username and password is correct
        if user:
            # check if user is staff or superuser
            if user.groups.filter(name='Manager').exists() or user.is_superuser:
                login(request, user)
                return redirect('manager:IndexView')
            else:
                return render(request, 'manager/login.html', context={'alert': 'You are not superuser or staff!!!', })
        else:
            return render(request, 'manager/login.html', context={'alert': 'The information is wrong!', })
    return render(request, 'manager/login.html')


# this view for logout staff or superuser to manager panel
def logout_view(request):
    # check the login user is staff or superuser
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
        logout(request)
    return redirect('manager:LoginView')


# this view for show taken exam
def user_answer_list(request):
    # check the login user is staff or superuser
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
        # get all taken exam order by time
        all_user_answers = models.UserAnswer.objects.all().order_by('-time')

        alert = ''
        # this part for filtering the taken exam
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
        # end filtering part

        context = {
            'all_user_answers': all_user_answers,
            'alert': alert,
        }
        return render(request, 'manager/user_answer.html', context=context)
    return redirect('manager:LoginView')


# this view for show all student
def user_list(request):
    # check the login user is staff or superuser
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
        # get all user in student group
        all_user = User.objects.filter(groups__name='Student')

        alert = ''
        # this part for filtering the user
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
        # end filtering part

        context = {
            'all_user': all_user,
            'alert': alert,
        }
        return render(request, 'manager/user.html', context)
    return redirect('manager:LoginView')


# this view for show information of user
def user_detail(request, pk):
    # check the login user is staff or superuser
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
        # get specific user that we want it
        current_user = User.objects.get(id=pk)
        # check this user has a profile
        current_profile = None
        if models.Profile.objects.filter(user=current_user):
            current_profile = models.Profile.objects.get(user=current_user)
        # get all taken exams of this user
        user_answers = models.UserAnswer.objects.filter(user=current_user)
        context = {
            'current_user': current_user,
            'current_profile': current_profile,
            'user_answers': user_answers,
        }
        return render(request, 'manager/user_detail.html', context)
    return redirect('manager:LoginView')


# this view for edit and delete specific user
def user_edit(request, pk):
    # check the login user is staff or superuser
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:

        # this part for delete this user
        if request.POST.get('delete_btn'):
            current_user = User.objects.get(id=pk)
            current_user.delete()
            return redirect('manager:UserList')

        # this part for edit this user information
        elif request.POST.get('edit_user_btn'):
            # get information send with post method
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')

            # get this user
            my_user = User.objects.get(id=pk)
            # get all user except this user
            all_users = User.objects.exclude(id=pk)
            # get all profile except for this user
            all_profiles = models.Profile.objects.exclude(user_id=pk)

            # this is for check username is unique or not
            username_exists = all_users.filter(username=username).exists()
            # this is for check email is unique or not
            email_exists = all_users.filter(email=email).exists()
            # this is for check phone number is unique or not
            phone_number_exists = all_profiles.filter(phone_number=phone_number).exists()

            # check username and email and phone number is unique
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

            # save new information for user
            my_user.username = username
            my_user.email = email
            my_user.first_name = first_name
            my_user.last_name = last_name

            my_user.save()

            # save new information for profile of this user
            # check this user has a profile
            if models.Profile.objects.filter(user_id=pk):
                my_profile = models.Profile.objects.get(user_id=pk)
                my_profile.phone_number = phone_number
                my_profile.address = address
                my_profile.save()
            else:
                models.Profile.objects.create(user=my_user, phone_number=phone_number, address=address)

            return redirect('manager:UserList')
        # get method
        else:
            user = User.objects.get(id=pk)
            context = {
                'user': user,
            }
            return render(request, 'manager/edit_user.html', context)
    return redirect('manager:LoginView')


# this view for show all exam
def exam_list(request):
    # check the login user is staff or superuser
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
        # get all exam
        all_exams = models.Exam.objects.all()

        alert = ''
        # this part for filtering the exam
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
            # end filtering part

        context = {
            'all_exams': all_exams,
            'alert': alert,
        }
        return render(request, 'manager/exam_list.html', context)
    return redirect('manager:LoginView')


# this view for create exam
def exam_create(request):
    # check the login user is staff or superuser
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
        # get exam information with post method
        if request.method == 'POST':
            book = request.POST.get('book')
            category = request.POST.get('category')
            difficulty = request.POST.get('difficulty')
            # save it
            models.Exam.objects.create(book_id=book, difficulty=difficulty, category=category)
            return redirect('manager:ExamList')
        else:
            all_books = models.Book.objects.all()
            context = {
                'all_books': all_books,
                'exam': models.Exam,
            }
            return render(request, 'manager/exam_create.html', context)
    return redirect('manager:LoginView')


# this view for delete and edit specific exam
def exam_edit(request, pk):
    # check the login user is staff or superuser
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:

        # the delete part
        if request.GET.get('delete_btn'):
            current_exam = models.Exam.objects.get(id=pk)
            current_exam.delete()
            return redirect('manager:ExamList')

        # the edit part
        elif request.POST.get('edit_exam_btn'):
            # get exam new information with post method
            book = request.POST.get('book')
            category = request.POST.get('category')
            difficulty = request.POST.get('difficulty')
            # image = None
            # if request.FILES:
            #     image = request.FILES['image']

            # save new information
            current_exam = models.Exam.objects.get(id=pk)
            current_exam.book.id = book
            current_exam.category = category
            current_exam.difficulty = difficulty
            # if image is not None:
            #     current_exam.image = image
            current_exam.save()

            return redirect('manager:ExamList')

        else:
            current_exam = models.Exam.objects.get(id=pk)
            all_books = models.Book.objects.all()
            context = {
                'current_exam': current_exam,
                'all_books': all_books,
                'exam': models.Exam,
            }
            return render(request, 'manager/exam_detail.html', context)
    return redirect('manager:LoginView')


# this view for send new ticket
def send_ticket(request):
    # check the login user is staff or superuser
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
        if request.method == 'POST':
            all_user = User.objects.all()
            text = request.POST.get('text')
            title = request.POST.get('title')
            subject = request.POST.get('subject')
            receivers = []
            # check text is empty
            if text is not None:
                for user in all_user:
                    # append selected user to an array list
                    if request.POST.get('receiver' + str(user.id)):
                        receivers.append(request.POST.get('receiver' + str(user.id)))
                # send and save this ticket for all selected user
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
    return redirect('manager:LoginView')


# this view for show all ticket
def ticket(request):
    # check the login user is staff or superuser
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
        # get all ticket
        all_tickets = models.Ticket.objects.all()

        alert = ''
        # this part for filtering the ticket
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
            # end filtering part
        context = {
            'alert': alert,
            'all_tickets': all_tickets,
        }
        return render(request, 'manager/ticket.html', context)
    return redirect('manager:LoginView')


# this view for show messages of a ticket or send message in ticket
def ticket_history(request, pk):
    # check the login user is staff or superuser
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
        # this part for send message
        if request.method == 'POST':
            text = request.POST.get('new_message')
            models.TicketMessage.objects.update_or_create(ticket_id=pk, text=text, sender=request.user)
        # end filtering part
        messages_for_ticket = models.TicketMessage.objects.filter(ticket_id=pk)
        context = {
            'messages_for_ticket': messages_for_ticket,
        }
        return render(request, 'manager/ticket_history.html', context)
    return redirect('manager:LoginView')


def reading_list(request):
    all_reading = models.Passage.objects.all()
    context = {
        'all_reading': all_reading,
    }
    return render(request, 'manager/reading_list.html', context)


def book_list(request):
    return render(request, 'manager/book_list.html')


def reading_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        exam = request.POST.get('exam')
        image = None
        if request.FILES:
            image = request.FILES['image']
        priority = request.POST.get('priority')
        text = request.POST.get('text')
        models.Passage.objects.create(title=title, exam_id=exam, image=image, priority=priority, text=text)
        print(text)
        return redirect('manager:ReadingList')
    all_exam = models.Exam.objects.all()
    context = {
        'all_exam': all_exam,
    }
    return render(request, 'manager/reading_create.html', context)


def reading_detail(request, pk):
    current_passage = models.Passage.objects.get(id=pk)
    context = {
        'current_passage': current_passage,
    }
    return render(request, 'manager/reading_detail.html', context)


def reading_edit(request, pk):
    return render(request, 'manager/reading_edit.html')
