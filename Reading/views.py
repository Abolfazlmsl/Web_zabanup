import json

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.contrib.auth.models import User
from django.template import loader

from . import models
# Create your views here.


# home page that check authentication
# if ok then render home page
# else redirect to login page
def home(request):
    # check user is authenticated
    if request.user.is_authenticated:
        username = request.user.username
        return render(request, 'Reading/home.html', context={'user': username})
    else:
        return redirect('Reading:Login')


# get passage details and render passage page if user is authenticated
def passage_body(request, passage_id):
    # check user is authenticated
    if request.user.is_authenticated:

        # this is use for refresh of submit page
        user_answer = models.UserAnswer.objects.all().count()

        # get passage and question of it
        passage = get_object_or_404(models.Passage, pk=passage_id)
        questions = get_list_or_404(models.Question, passage=passage)

        # define for add our questions to these list
        dropdown = []
        textbox = []
        radiobutton = []
        checkbox = []

        # add same question to 4 different lists
        for question in questions:
            # dropdown questions
            if question.type == 'dropdown':
                dropdown.append(question)
            # textbox questions
            elif question.type == 'text':
                textbox.append(question)
            # radiobutton questions
            elif question.type == 'radiobutton':
                radiobutton.append(question)
            # checkbox questions
            elif question.type == 'checkbox':
                checkbox.append(question)

        # get text in html form then render it
        ht = str(passage.text)
        template = loader.get_template(ht).render()
        print(passage.text.url)
        exam = models.Exam.objects.filter(reading=passage)[0]
        print(exam)
        # create a context
        context = {
            'passage': passage,
            'dropdown': dropdown,
            'textbox': textbox,
            'radiobutton': radiobutton,
            'checkbox': checkbox,
            'exam': exam,
            'temp': template,
            'refresh_checker': user_answer + 1,
        }
        return render(request, 'Reading/passages.html', context=context)
    else:
        return redirect('Reading:Login')


# calculate grade and submit comments
def submit(request, passage_id):
    # calculate grade
    if request.POST.get('Submit'):
        # get passage and question
        passage = get_object_or_404(models.Passage, pk=passage_id)
        questions = get_list_or_404(models.Question, passage=passage)
        refresh_checker = request.POST.get('refresh_checker')
        # initial counter for each type of question
        dropdown_count = 0
        textbox_count = 0
        radiobutton_count = 0
        checkbox_count = 0
        # initial list for each type of question
        dropdown_list = []
        textbox_list = []
        radiobutton_list = []
        checkbox_list = []
        correct_answers = []

        grade = 0

        # calculate question of each type
        for question in questions:
            if question.type == 'dropdown':
                dropdown_count += 1
            elif question.type == 'text':
                textbox_count += 1
            elif question.type == 'radiobutton':
                radiobutton_count += 1
            elif question.type == 'checkbox':
                checkbox_count += 1

        # get user answers
        # get  user answer id of questions
        for i in range(dropdown_count):
            plus = str(i+1)
            answer_id = request.POST.get('q' + plus)
            dropdown_list.append(answer_id)
        for i in range(textbox_count):
            # hidden_plus used for get text box question id
            hidden_plus = str(i+1)
            plus = str(i+1+dropdown_count)
            answer_text = request.POST.get('q' + plus)
            question_id = request.POST.get('hidden' + hidden_plus)
            textbox_list.append([question_id, answer_text])
        for i in range(radiobutton_count):
            plus = str(i+1+dropdown_count+textbox_count)
            answer_id = request.POST.get('q' + plus)
            radiobutton_list.append(answer_id)
        for i in range(checkbox_count):
            plus = str(i+1+dropdown_count+textbox_count+radiobutton_count)
            answer_id = request.POST.getlist('q' + plus)
            question_id = request.POST.get('q' + plus + '_id')
            checkbox_list.append([question_id, answer_id])

        # calculate correct answers and grade
        for answer in dropdown_list:
            if answer:
                my_answer = get_object_or_404(models.Answer, id=answer).truth
                if my_answer:
                    correct_answers.append(get_object_or_404(models.Answer, id=answer).question_id)
                    grade += 1

        for answer in textbox_list:
            if answer[1] == get_object_or_404(models.Answer, question=answer[0]).text:
                correct_answers.append(int(answer[0]))
                grade += 1

        for answer in radiobutton_list:
            if answer:
                my_answer = get_object_or_404(models.Answer, id=answer).truth
                if my_answer:
                    correct_answers.append(get_object_or_404(models.Answer, id=answer).question_id)
                    grade += 1

        for i in checkbox_list:
            count_q = 0
            question = get_object_or_404(models.Question, id=i[0])
            answers_q = get_list_or_404(models.Answer, question=question)
            for answer in answers_q:
                if answer.truth:
                    count_q += 1
            for answer in i[1]:
                if get_object_or_404(models.Answer, id=answer).truth:
                    count_q -= 1
                else:
                    count_q += 1
            if count_q == 0:
                correct_answers.append(int(i[0]))
                grade += 1

        multi_number = 100 / passage.question_set.all().__len__()
        final_grade = grade*multi_number

        # create a json from answers
        save_list = {}
        for question in passage.question_set.all():
            if question.id in correct_answers:
                save_list[str(question.id)] = "correct"
            else:
                save_list[str(question.id)] = "wrong"
        save_list = json.dumps(save_list)
        # save user grade
        models.UserAnswer.objects.update_or_create(user=request.user, passage=passage, grade=final_grade,
                                                   answer=str(save_list), counter=refresh_checker)
        users_answer = models.UserAnswer.objects.filter(passage=passage).order_by('-grade')
        last_user_answer = models.UserAnswer.objects.filter(passage=passage, user=request.user).last()
        if models.Comment.objects.filter(passage=passage):
            all_comments = models.Comment.objects.filter(passage=passage)
        else:
            all_comments = []
        context = {
            'passage': passage,
            'grade': final_grade,
            'correct_answers': correct_answers,
            'users_answer': users_answer,
            'last_user_answer': last_user_answer,
            'all_comments': all_comments,
            'comment': 0,
        }
        return render(request, 'Reading/submit.html', context)

    elif request.POST.get('comment-submit'):

        passage = models.Passage.objects.get(id=passage_id)
        users_answer = models.UserAnswer.objects.filter(passage=passage).order_by('-grade')
        last_answer = get_list_or_404(models.UserAnswer, passage=passage, user=request.user).pop()

        comment_text = request.POST.get('comment_text')
        # change user answer to json
        my_answer = last_answer.answer
        my_answer = json.loads(my_answer)
        my_answers = []
        for i in my_answer:
            my_answers.append(my_answer[i])

        last_user_answer = last_answer
        # add user comment to database
        if comment_text:
            models.Comment.objects.update_or_create(passage=passage, text=comment_text, user=request.user)

        final_grade = last_answer.grade
        # get all comments of passage from database
        if models.Comment.objects.filter(passage=passage):
            all_comments = models.Comment.objects.filter(passage=passage)
        else:
            all_comments = []

        context = {
            'passage': passage,
            'grade': final_grade,
            'users_answer': users_answer,
            'my_answer': my_answers,
            'last_user_answer': last_user_answer,
            'comment': 1,
            'all_comments': all_comments,
        }
        return render(request, 'Reading/submit.html', context)

    elif request.POST.get('reply-submit'):

        passage = models.Passage.objects.get(id=passage_id)
        users_answer = models.UserAnswer.objects.filter(passage=passage).order_by('-grade')
        last_answer = get_list_or_404(models.UserAnswer, passage=passage, user=request.user).pop()
        # get reply text and parent id of that reply
        reply_text = request.POST.get('reply-text')
        reply_parent_id = request.POST.get('hidden-reply')
        reply_to = models.Comment.objects.get(id=reply_parent_id)

        my_answer = last_answer.answer
        my_answer = json.loads(my_answer)
        my_answers = []
        for i in my_answer:
            my_answers.append(my_answer[i])

        last_user_answer = last_answer
        # save reply to database
        models.Comment.objects.update_or_create(passage=passage, text=reply_text, user=request.user, parent=reply_to)

        final_grade = last_answer.grade
        if models.Comment.objects.filter(passage=passage):
            all_comments = models.Comment.objects.filter(passage=passage)
        else:
            all_comments = []

        context = {
            'passage': passage,
            'grade': final_grade,
            'users_answer': users_answer,
            'my_answer': my_answers,
            'last_user_answer': last_user_answer,
            'comment': 1,
            'all_comments': all_comments,
        }

        return render(request, 'Reading/submit.html', context)

    else:
        
        passage = models.Passage.objects.get(id=passage_id)
        users_answer = models.UserAnswer.objects.filter(passage=passage).order_by('-grade')
        last_answer = get_list_or_404(models.UserAnswer, passage=passage, user=request.user).pop()

        my_answer = last_answer.answer
        my_answer = json.loads(my_answer)
        my_answers = []
        for i in my_answer:
            my_answers.append(my_answer[i])

        last_user_answer = last_answer
        final_grade = last_answer.grade

        if models.Comment.objects.filter(passage=passage):
            all_comments = models.Comment.objects.filter(passage=passage)
        else:
            all_comments = []

        context = {
            'passage': passage,
            'grade': final_grade,
            'users_answer': users_answer,
            'my_answer': my_answers,
            'last_user_answer': last_user_answer,
            'comment': 1,
            'all_comments': all_comments,
        }

        return render(request, 'Reading/submit.html', context)


# login to website
def login_view(request):
    # check our method is post
    if request.method == 'POST':
        # get username and password
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # check has this user or not
        if user:
            login(request, user)
            return redirect('Reading:home')
        else:
            return render(request, 'Reading/login.html', context={'alert': 'The information is wrong!', })
    else:
        return render(request, 'Reading/login.html', context={})


# logout from website
def logout_view(request):
    logout(request)
    return redirect('Reading:home')


# change password of user
def change_password(request):
    # check our method is post
    if request.method == 'POST':
        # get currently user
        u = User.objects.get(username=request.user.username)
        # get new password write by user and save it in db
        newpass = request.POST['newpass']
        u.set_password(newpass)
        u.save()
        return redirect('Reading:submit')
    else:
        return render(request, 'Reading/change_password.html')


# signup of user
def signup_view(request):
    if request.method == 'POST':
        # get all user information
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        address = request.POST.get('address')
        # check password and verify password be same
        if password != re_password:
            context = {
                'alert': 'Passwords does not match!',
            }
            return render(request, 'Reading/signup.html', context)
        else:
            us = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username,
                                          password=password)
            us.save()
            models.Profile(user=us, phone_number=phone_number, address=address).save()
            return redirect('Reading:Login')
    else:
        return render(request, 'Reading/signup.html')


# show and filter exams
def exam(request):
    # check method
    if request.POST:
        # get current user
        username = request.user.username

        # get all books
        # the filters doesn't chose return none
        all_books = []
        for book in models.Exam.BOOK_List:
            all_books.append(request.POST.get(book[0]))
        # get filter that chose by user
        filter_book = []
        for book in all_books:
            if book:
                filter_book.append(book)

        # get all categories
        # the filters doesn't chose return none
        all_categories = []
        for category in models.Exam.CATEGORY:
            all_categories.append(request.POST.get(category[0]))
        # get filter that chose by user
        filter_category = []
        for category in all_categories:
            if category:
                filter_category.append(category)

        # get all difficulties
        # the filters doesn't chose return none
        all_difficulties = []
        for difficulty in models.Exam.DIFFICULTY:
            all_difficulties.append(request.POST.get(difficulty[0]))
        # get filter that chose by user
        filter_difficulty = []
        for difficulty in all_difficulties:
            if difficulty:
                filter_difficulty.append(difficulty)

        # filter exams
        exams = []
        # check if we have filter by book
        if len(filter_book) > 0:
            exams = models.Exam.objects.filter(book__in=filter_book)
        # check if we have filter by category
        if len(filter_category) > 0:
            exams = models.Exam.objects.filter(category__in=filter_category)
        # check if we have filter by difficulty
        if len(filter_difficulty) > 0:
            exams = models.Exam.objects.filter(difficulty__in=filter_difficulty)
        # if don't chose any filter then select all exams
        if len(filter_difficulty) == 0 and len(filter_category) == 0 and len(filter_book) == 0:
            exams = get_list_or_404(models.Exam)

        exam_filter = models.Exam

        # create context
        context = {
            'exam_filter': exam_filter,
            'exams': exams,
        }

        return render(request, 'Reading/filter.html', context=context)
    else:
        exams = get_list_or_404(models.Exam)
        exam_filter = models.Exam
        context = {
            'exams': exams,
            'exam_filter': exam_filter,
        }
        return render(request, 'Reading/filter.html', context=context)
