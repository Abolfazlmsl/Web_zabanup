import json

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.contrib.auth.models import User
from django.template import loader

from . import models


# Create your views here.


# get passage details and render passage page if user is authenticated
def passage_body(request, exam_id):
    # check user is authenticated
    if request.user.is_authenticated:
        # this is use for refresh of submit page
        user_answer = models.UserAnswer.objects.all().count()

        # get passage and question of it
        current_exam = models.Exam.objects.get(id=exam_id)
        all_passages = models.Passage.objects.filter(exam=current_exam)
        passage1 = all_passages[0]
        passage2 = all_passages[1]
        passage3 = all_passages[2]
        # print(passage1)
        # print(passage2)
        # print(passage3)

        # define for add our questions to these list
        dropdown_passage1 = []
        textbox_passage1 = []
        radiobutton_passage1 = []
        checkbox_passage1 = []

        dropdown_passage2 = []
        textbox_passage2 = []
        radiobutton_passage2 = []
        checkbox_passage2 = []

        dropdown_passage3 = []
        textbox_passage3 = []
        radiobutton_passage3 = []
        checkbox_passage3 = []

        # add same question to 4 different lists
        add_question_to_list(passage1, dropdown_passage1, textbox_passage1, radiobutton_passage1, checkbox_passage1)
        add_question_to_list(passage2, dropdown_passage2, textbox_passage2, radiobutton_passage2, checkbox_passage2)
        add_question_to_list(passage3, dropdown_passage3, textbox_passage3, radiobutton_passage3, checkbox_passage3)

        # get text in html form then render it
        html_for_passage1 = str(passage1.text)
        template1 = loader.get_template(html_for_passage1).render()
        html_for_passage2 = str(passage2.text)
        template2 = loader.get_template(html_for_passage2).render()
        html_for_passage3 = str(passage3.text)
        template3 = loader.get_template(html_for_passage3).render()
        # create a context
        # print(dropdown_passage1[0].type)
        # print(dropdown_passage2)
        # print(dropdown_passage3)
        # print(textbox_passage1)
        # print(textbox_passage2)
        # print(textbox_passage3)
        # print(radiobutton_passage1)
        # print(radiobutton_passage2)
        # print(radiobutton_passage3)
        # print(checkbox_passage1)
        # print(checkbox_passage2)
        # print(checkbox_passage3)

        number_of_dd_p1 = len(dropdown_passage1)
        number_of_tb_p1 = len(textbox_passage1)
        number_of_rb_p1 = len(radiobutton_passage1)
        number_of_cb_p1 = len(checkbox_passage1)

        number_of_dd_p2 = len(dropdown_passage2)
        number_of_tb_p2 = len(textbox_passage2)
        number_of_rb_p2 = len(radiobutton_passage2)
        number_of_cb_p2 = len(checkbox_passage2)

        number_of_dd_p3 = len(dropdown_passage3)
        number_of_tb_p3 = len(textbox_passage3)
        number_of_rb_p3 = len(radiobutton_passage3)
        number_of_cb_p3 = len(checkbox_passage3)

        number_of_q_p1 = len(dropdown_passage1 + textbox_passage1 + checkbox_passage1 + checkbox_passage1)
        number_of_q_p2 = len(dropdown_passage2 + textbox_passage2 + checkbox_passage2 + checkbox_passage2)
        number_of_q_p3 = len(dropdown_passage3 + textbox_passage3 + checkbox_passage3 + checkbox_passage3)

        context = {
            'dropdown_passage1': dropdown_passage1,
            'textbox_passage1': textbox_passage1,
            'radiobutton_passage1': radiobutton_passage1,
            'checkbox_passage1': checkbox_passage1,

            'dropdown_passage2': dropdown_passage2,
            'textbox_passage2': textbox_passage2,
            'radiobutton_passage2': radiobutton_passage2,
            'checkbox_passage2': checkbox_passage2,

            'dropdown_passage3': dropdown_passage3,
            'textbox_passage3': textbox_passage3,
            'radiobutton_passage3': radiobutton_passage3,
            'checkbox_passage3': checkbox_passage3,

            'template1': template1,
            'template2': template2,
            'template3': template3,

            'refresh_checker': user_answer + 1,
            'current_exam': current_exam,

            'passage1': passage1,
            'passage2': passage2,
            'passage3': passage3,

            'number_of_q_p1': number_of_q_p1,
            'number_of_q_p2': number_of_q_p2,
            'number_of_q_p3': number_of_q_p3,

            'number_of_dd_p1': number_of_dd_p1,
            'number_of_tb_p1': number_of_tb_p1,
            'number_of_rb_p1': number_of_rb_p1,
            'number_of_cb_p1': number_of_cb_p1,
            'number_of_dd_p2': number_of_dd_p2,
            'number_of_tb_p2': number_of_tb_p2,
            'number_of_rb_p2': number_of_rb_p2,
            'number_of_cb_p2': number_of_cb_p2,
            'number_of_dd_p3': number_of_dd_p3,
            'number_of_tb_p3': number_of_tb_p3,
            'number_of_rb_p3': number_of_rb_p3,
            'number_of_cb_p3': number_of_cb_p3,
        }
        return render(request, 'Reading/passages.html', context=context)
    else:
        return redirect('Reading:Login')


def add_question_to_list(passage, dd, tb, rb, cb):
    questions = get_list_or_404(models.Question, passage=passage)
    for question in questions:
        # dropdown questions
        if question.type == 'dropdown':
            dd.append(question)
        # textbox questions
        elif question.type == 'text':
            tb.append(question)
        # radiobutton questions
        elif question.type == 'radiobutton':
            rb.append(question)
        # checkbox questions
        elif question.type == 'checkbox':
            cb.append(question)


# calculate grade and submit comments
def submit(request, exam_id):
    # calculate grade
    if request.POST.get('Submit'):
        # get passage and question
        current_exam = models.Exam.objects.get(id=exam_id)

        all_passages = current_exam.passage_set.all()

        passage1 = all_passages[0]
        passage2 = all_passages[1]
        passage3 = all_passages[2]

        passage1_questions = get_list_or_404(models.Question, passage=passage1)
        passage2_questions = get_list_or_404(models.Question, passage=passage2)
        passage3_questions = get_list_or_404(models.Question, passage=passage3)

        refresh_checker = request.POST.get('refresh_checker')

        # initial counter for each type of question
        dropdown1_count = 0
        textbox1_count = 0
        radiobutton1_count = 0
        checkbox1_count = 0

        dropdown2_count = 0
        textbox2_count = 0
        radiobutton2_count = 0
        checkbox2_count = 0

        dropdown3_count = 0
        textbox3_count = 0
        radiobutton3_count = 0
        checkbox3_count = 0

        # initial list for each type of question
        dropdown_list = []
        textbox_list = []
        radiobutton_list = []
        checkbox_list = []
        correct_answers = []

        grade = 0

        # calculate question of each type
        for question in passage1_questions:
            if question.type == 'dropdown':
                dropdown1_count += 1
            elif question.type == 'text':
                textbox1_count += 1
            elif question.type == 'radiobutton':
                radiobutton1_count += 1
            elif question.type == 'checkbox':
                checkbox1_count += 1

        for question in passage2_questions:
            if question.type == 'dropdown':
                dropdown2_count += 1
            elif question.type == 'text':
                textbox2_count += 1
            elif question.type == 'radiobutton':
                radiobutton2_count += 1
            elif question.type == 'checkbox':
                checkbox2_count += 1

        for question in passage3_questions:
            if question.type == 'dropdown':
                dropdown3_count += 1
            elif question.type == 'text':
                textbox3_count += 1
            elif question.type == 'radiobutton':
                radiobutton3_count += 1
            elif question.type == 'checkbox':
                checkbox3_count += 1

        # get user answers
        # get  user answer id of questions
        for i in range(dropdown1_count):
            plus = str(i + 1)
            answer_id = request.POST.get('q' + plus)
            dropdown_list.append(answer_id)

        for i in range(dropdown2_count):
            plus = str(i + 1 +len(passage1_questions))
            answer_id = request.POST.get('q' + plus)
            dropdown_list.append(answer_id)

        for i in range(dropdown3_count):
            plus = str(i + 1 + len(passage1_questions) + len(passage2_questions))
            answer_id = request.POST.get('q' + plus)
            dropdown_list.append(answer_id)

        for i in range(textbox1_count):
            # hidden_plus used for get text box question id
            hidden_plus = str(i + 1)
            plus = str(i + 1 + dropdown1_count)
            answer_text = request.POST.get('q' + plus)
            question_id = request.POST.get('hidden' + hidden_plus)
            textbox_list.append([question_id, answer_text])

        for i in range(textbox2_count):
            # hidden_plus used for get text box question id
            hidden_plus = str(i + 1 + textbox1_count)
            plus = str(i + 1 + len(passage1_questions) + dropdown2_count)
            answer_text = request.POST.get('q' + plus)
            question_id = request.POST.get('hidden' + hidden_plus)
            textbox_list.append([question_id, answer_text])

        for i in range(textbox3_count):
            # hidden_plus used for get text box question id
            hidden_plus = str(i + 1 + textbox1_count + textbox2_count)
            plus = str(i + 1 + len(passage1_questions) + len(passage2_questions) + dropdown3_count)
            answer_text = request.POST.get('q' + plus)
            question_id = request.POST.get('hidden' + hidden_plus)
            textbox_list.append([question_id, answer_text])

        for i in range(radiobutton1_count):
            plus = str(i + 1 + dropdown1_count + textbox1_count)
            answer_id = request.POST.get('q' + plus)
            radiobutton_list.append(answer_id)

        for i in range(radiobutton2_count):
            plus = str(i + 1 + len(passage1_questions) + dropdown2_count + textbox2_count)
            answer_id = request.POST.get('q' + plus)
            radiobutton_list.append(answer_id)

        for i in range(radiobutton3_count):
            plus = str(i + 1 + len(passage1_questions) + len(passage2_questions) + dropdown3_count + textbox3_count)
            answer_id = request.POST.get('q' + plus)
            radiobutton_list.append(answer_id)

        for i in range(checkbox1_count):
            plus = str(i + 1 + dropdown1_count + textbox1_count + radiobutton1_count)
            answer_id = request.POST.getlist('q' + plus)
            question_id = request.POST.get('q' + plus + '_id')
            checkbox_list.append([question_id, answer_id])

        for i in range(checkbox2_count):
            plus = str(i + 1 + len(passage1_questions) + dropdown2_count + textbox2_count + radiobutton2_count)
            answer_id = request.POST.getlist('q' + plus)
            question_id = request.POST.get('q' + plus + '_id')
            checkbox_list.append([question_id, answer_id])

        for i in range(checkbox3_count):
            plus = str(i + 1 + len(passage1_questions) + len(passage2_questions) + dropdown3_count + textbox3_count + radiobutton3_count)
            answer_id = request.POST.getlist('q' + plus)
            question_id = request.POST.get('q' + plus + '_id')
            checkbox_list.append([question_id, answer_id])

        print(dropdown_list)
        print(textbox_list)
        print(radiobutton_list)
        print(checkbox_list)
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

        multi_number = 100 / len(passage1_questions + passage2_questions + passage3_questions)
        all_questions = passage1_questions + passage2_questions + passage3_questions
        print(all_questions)
        final_grade = grade * multi_number
        final_grade = round(final_grade, 2)

        # create a json from answers
        save_list = {}
        for question in passage1_questions:
            if question.id in correct_answers:
                save_list[str(question.id)] = "correct"
            else:
                save_list[str(question.id)] = "wrong"
        for question in passage2_questions:
            if question.id in correct_answers:
                save_list[str(question.id)] = "correct"
            else:
                save_list[str(question.id)] = "wrong"
        for question in passage3_questions:
            if question.id in correct_answers:
                save_list[str(question.id)] = "correct"
            else:
                save_list[str(question.id)] = "wrong"
        save_list = json.dumps(save_list)
        # save user grade
        models.UserAnswer.objects.update_or_create(user=request.user, exam=current_exam, grade=final_grade,
                                                   answer=str(save_list), counter=refresh_checker)
        users_answer = models.UserAnswer.objects.filter(exam=current_exam).order_by('-grade')
        last_user_answer = models.UserAnswer.objects.filter(exam=current_exam, user=request.user).last()
        if models.Comment.objects.filter(exam=current_exam):
            all_comments = models.Comment.objects.filter(exam=current_exam)
        else:
            all_comments = []
        context = {
            'all_questions': all_questions,
            'passage': passage1,
            'grade': final_grade,
            'correct_answers': correct_answers,
            'users_answer': users_answer,
            'last_user_answer': last_user_answer,
            'all_comments': all_comments,
            'exam': current_exam,
            'comment': 0,
        }
        return render(request, 'Reading/submit.html', context)

    elif request.POST.get('comment-submit'):

        current_exam = models.Exam.objects.get(id=exam_id)
        users_answer = models.UserAnswer.objects.filter(exam=current_exam).order_by('-grade')
        last_answer = get_list_or_404(models.UserAnswer, exam=current_exam, user=request.user).pop()

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
            models.Comment.objects.update_or_create(exam=current_exam, text=comment_text, user=request.user)

        final_grade = last_answer.grade
        # get all comments of passage from database
        if models.Comment.objects.filter(exam=current_exam):
            all_comments = models.Comment.objects.filter(exam=current_exam)
        else:
            all_comments = []

        context = {
            'exam': current_exam,
            'grade': final_grade,
            'users_answer': users_answer,
            'my_answer': my_answers,
            'last_user_answer': last_user_answer,
            'comment': 1,
            'all_comments': all_comments,
        }
        return render(request, 'Reading/submit.html', context)

    elif request.POST.get('reply-submit'):

        current_exam = models.Exam.objects.get(id=exam_id)
        users_answer = models.UserAnswer.objects.filter(exam=current_exam).order_by('-grade')
        last_answer = get_list_or_404(models.UserAnswer, exam=current_exam, user=request.user).pop()
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
        models.Comment.objects.update_or_create(exam=current_exam, text=reply_text, user=request.user, parent=reply_to)

        final_grade = last_answer.grade
        if models.Comment.objects.filter(exam=current_exam):
            all_comments = models.Comment.objects.filter(exam=current_exam)
        else:
            all_comments = []

        context = {
            'exam': current_exam,
            'grade': final_grade,
            'users_answer': users_answer,
            'my_answer': my_answers,
            'last_user_answer': last_user_answer,
            'comment': 1,
            'all_comments': all_comments,
        }

        return render(request, 'Reading/submit.html', context)

    else:

        current_exam = models.Exam.objects.get(id=exam_id)
        users_answer = models.UserAnswer.objects.filter(exam=current_exam).order_by('-grade')
        last_answer = get_list_or_404(models.UserAnswer, exam=current_exam, user=request.user).pop()

        my_answer = last_answer.answer
        my_answer = json.loads(my_answer)
        my_answers = []
        for i in my_answer:
            my_answers.append(my_answer[i])

        last_user_answer = last_answer
        final_grade = last_answer.grade

        if models.Comment.objects.filter(exam=current_exam):
            all_comments = models.Comment.objects.filter(exam=current_exam)
        else:
            all_comments = []

        context = {
            'exam': current_exam,
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
        return redirect('Reading:home')
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
    if request.user.is_authenticated:
        # check method
        if request.POST:
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
    else:
        return redirect('Reading:Login')