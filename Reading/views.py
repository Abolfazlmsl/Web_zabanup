import json

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.contrib.auth.models import User
from django.template import loader
from django.urls import reverse

from . import models
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        username = request.user.username
        return render(request, 'home.html', context={'user': username})
    else:
        return redirect('Reading:Login')


def reading(request):
    if request.user.is_authenticated:
        exams = models.Exam.objects.all()
        context = {'exams': exams}
        return render(request, 'filter.html', context)
    else:
        return redirect('Reading:home')


def passage_body(request, passage_id):
    if request.user.is_authenticated:
        user_answer = models.UserAnswer.objects.all().count()
        passage = get_object_or_404(models.Passage, pk=passage_id)
        questions = get_list_or_404(models.Question, passage=passage)
        dropdown = []
        textbox = []
        radiobutton = []
        checkbox = []
        for question in questions:
            if question.type == 'dropdown':
                dropdown.append(question)
            elif question.type == 'text':
                textbox.append(question)
            elif question.type == 'radiobutton':
                radiobutton.append(question)
            elif question.type == 'checkbox':
                checkbox.append(question)
        ht = str(passage.text)
        template = loader.get_template(ht).render()
        context = {
            'passage': passage,
            'dropdown': dropdown,
            'textbox': textbox,
            'radiobutton': radiobutton,
            'checkbox': checkbox,
            'temp': template,
            'refresh_checker': user_answer + 1,
        }
        return render(request, 'Reading/passages.html', context=context)
    else:
        return redirect('Reading:Login')


def submit(request, passage_id):
    # if request.method == 'POST':
    if request.POST.get('Submit'):
        passage = get_object_or_404(models.Passage, pk=passage_id)
        questions = get_list_or_404(models.Question, passage=passage)
        refresh_checker = request.POST.get('refresh_checker')
        dropdown_count = 0
        textbox_count = 0
        radiobutton_count = 0
        checkbox_count = 0
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

        for i in range(dropdown_count):
            plus = str(i+1)
            q = request.POST.get('q' + plus)
            dropdown_list.append(q)
        for i in range(textbox_count):
            iplus = str(i+1)
            plus = str(i+1+dropdown_count)
            q = request.POST.get('q' + plus)
            h = request.POST.get('hidden' + iplus)
            textbox_list.append([h, q])
        for i in range(radiobutton_count):
            plus = str(i+1+dropdown_count+textbox_count)
            q = request.POST.get('q' + plus)
            radiobutton_list.append(q)
        for i in range(checkbox_count):
            plus = str(i+1+dropdown_count+textbox_count+radiobutton_count)
            q = request.POST.getlist('q' + plus)
            h = request.POST.get('q' + plus + '_id')
            checkbox_list.append([h, q])

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
        save_list = {}
        for question in passage.question_set.all():
            if question.id in correct_answers:
                save_list[str(question.id)] = "correct"
            else:
                save_list[str(question.id)] = "wrong"
        save_list = json.dumps(save_list)
        models.UserAnswer.objects.update_or_create(user=request.user, passage=passage, grade=final_grade,
                                                   answer=str(save_list), counter=refresh_checker)
        users_answer = models.UserAnswer.objects.all().order_by('-grade')
        last_user_answer = models.UserAnswer.objects.filter(passage=passage, user=request.user).last()
        context = {
            'passage': passage,
            'grade': final_grade,
            'correct_answers': correct_answers,
            'users_answer': users_answer,
            'last_user_answer': last_user_answer,
            'comment': 0,
        }

        return render(request, 'Reading/submit.html', context)





    elif request.POST.get('comment-submit'):
        print(52)
        passage = models.Passage.objects.get(id=passage_id)
        users_answer = models.UserAnswer.objects.filter(passage=passage, user=request.user).order_by('-time')
        print(users_answer)
        comment_text = request.POST.get('comment_text')
        my_answer = users_answer[0].answer
        my_answer = json.loads(my_answer)
        my_answers = []
        # print(my_answer)
        for i in my_answer:
            print(i)
            my_answers.append(my_answer[i])
        last_user_answer = users_answer[0]
        print(comment_text)
        if comment_text:
            print(1)
            models.Comment.objects.update_or_create(passage=passage, text=comment_text, user=request.user)
        final_grade = users_answer[0].grade
        print(final_grade)

        all_comments = get_list_or_404(models.Comment, passage=passage)
        context = {
            'passage': passage,
            'grade': final_grade,
            'users_answer': users_answer,
            'my_answer': my_answers,
            'last_user_answer': last_user_answer,
            'comment': 1,
            'all_comments': all_comments
        }
        return render(request, 'Reading/submit.html', context)

    elif request.POST.get('reply-submit'):
        print(77)
        passage = models.Passage.objects.get(id=passage_id)
        users_answer = models.UserAnswer.objects.filter(passage=passage, user=request.user).order_by('-time')
        reply_text = request.POST.get('reply-text')
        reply_parent_id = request.POST.get('hidden-reply')
        print(reply_text,reply_parent_id)
        # if request.POST.get('hidden-reply68'):
        #     print('nanaz')
        # else :
        #     print('agueru')
        # print(reply_parent_id)
        reply_to = models.Comment.objects.get(id=reply_parent_id)
        my_answer = users_answer[0].answer
        my_answer = json.loads(my_answer)
        my_answers = []
        for i in my_answer:
            my_answers.append(my_answer[i])
        last_user_answer = users_answer[0]
        models.Comment.objects.update_or_create(passage=passage, text=reply_text, user=request.user, parent=reply_to)
        final_grade = users_answer[0].grade
        all_comments = get_list_or_404(models.Comment, passage=passage)
        context = {
            'passage': passage,
            'grade': final_grade,
            'users_answer': users_answer,
            'my_answer': my_answers,
            'last_user_answer': last_user_answer,
            'comment': 1,
            'all_comments': all_comments
        }

        return render(request, 'Reading/submit.html', context)

    else:
        return render(request, 'Reading/submit.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('Reading:home')
        else:
            return render(request, 'login.html', context={'alert': 'The information is wrong!', })
    else:
        return render(request, 'login.html', context={})


def logout_view(request):
    logout(request)
    return redirect('Reading:home')


def change_password(request):
    if request.method == 'POST':
        u = User.objects.get(username=request.user.username)
        newpass = request.POST['newpass']
        u.set_password(newpass)
        u.save()
        return redirect('Reading:submit')
    else:
        return render(request, 'change_password.html')


def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        address = request.POST.get('address')
        if password != re_password:
            context = {
                'alert': 'Passwords does not match!',
            }
            return render(request, 'signup.html', context)
        else:
            us = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username,
                                          password=password)
            us.save()
            models.Profile(user=us, phone_number=phone_number, address=address).save()
            return redirect('Reading:Login')
    else:
        return render(request, 'signup.html')


def exam(request):
    if request.POST:
        username = request.user.username
        all_books = []
        for book in models.Exam.BOOK_List:
            all_books.append(request.POST.get(book[0]))
        filter_book = []
        for book in all_books:
            if book:
                filter_book.append(book)

        all_categories = []
        for category in models.Exam.CATEGORY:
            all_categories.append(request.POST.get(category[0]))
        filter_category = []
        for category in all_categories:
            if category:
                filter_category.append(category)

        all_difficulties = []
        for difficulty in models.Exam.DIFFICULTY:
            all_difficulties.append(request.POST.get(difficulty[0]))
        filter_difficulty = []
        for difficulty in all_difficulties:
            if difficulty:
                filter_difficulty.append(difficulty)

        print(filter_book)
        print(filter_category)
        print(filter_difficulty)

        exams = []
        if len(filter_book) > 0:
            exams = models.Exam.objects.filter(book__in=filter_book)
        if len(filter_category) > 0:
            exams = models.Exam.objects.filter(category__in=filter_category)
        if len(filter_difficulty) > 0:
            exams = models.Exam.objects.filter(difficulty__in=filter_difficulty)
        if len(filter_difficulty) == 0 and len(filter_category) == 0 and len(filter_book) == 0:
            exams = get_list_or_404(models.Exam)

        exam_filter = models.Exam
        context = {
            'exam_filter': exam_filter,
            'exams': exams,
        }
        print(1)
        return render(request, 'filter.html', context=context)
    else:
        exams = get_list_or_404(models.Exam)
        exam_filter = models.Exam
        print(1)
        context = {
            'exams': exams,
            'exam_filter': exam_filter,
        }
        return render(request, 'filter.html', context=context)
