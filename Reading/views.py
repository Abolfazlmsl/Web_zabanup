import json
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import loader
from . import models


# Create your views here.

# get passage details and render passage page if user is authenticated
# @login_required(login_url="/login")
def passage_body(request, exam_id):
    # check user is authenticated
    # this is use for refresh of submit page
    user_answer = models.UserAnswer.objects.all().count()

    # get passage and question of it
    current_exam = models.Exam.objects.get(id=exam_id)
    all_passages = models.Passage.objects.filter(exam=current_exam).order_by('priority')

    all_questions = []
    question_type = []
    i: int = 0
    j: int = 0
    questions_bound = []
    bound_temp = 1
    for passage in all_passages:
        questions = models.Question.objects.filter(passage=passage).order_by('priority')
        questions_bound.append(str(bound_temp) + '-' + str(len(questions) + bound_temp - 1))
        bound_temp += len(questions)
        yes_no_list = []
        true_false_list = []
        textbox_list = []
        matching_heading_list = []
        matching_paragraph_list = []
        summary_completion_list = []
        radiobutton_list = []
        checkbox_list = []
        temp_type = []
        for question in questions:
            j += 1
            if question.type == 'yesno':
                yes_no_list.append((question.priority, question, j))
                if question.type not in temp_type:
                    temp_type.append(question.type)
            elif question.type == 'truefalse':
                true_false_list.append((question.priority, question, j))
                if question.type not in temp_type:
                    temp_type.append(question.type)
            elif question.type == 'text':
                textbox_list.append((question.priority, question, j))
                if question.type not in temp_type:
                    temp_type.append(question.type)
            elif question.type == 'matching_heading':
                matching_heading_list.append((question.priority, question, j))
                if question.type not in temp_type:
                    temp_type.append(question.type)
            elif question.type == 'matching_paragraph':
                matching_paragraph_list.append((question.priority, question, j))
                if question.type not in temp_type:
                    temp_type.append(question.type)
            elif question.type == 'summary_completion':
                summary_completion_list.append((question.priority, question, j))
                if question.type not in temp_type:
                    temp_type.append(question.type)
            elif question.type == 'radiobutton':
                radiobutton_list.append((question.priority, question, j))
                if question.type not in temp_type:
                    temp_type.append(question.type)
            elif question.type == 'checkbox':
                checkbox_list.append((question.priority, question, j))
                if question.type not in temp_type:
                    temp_type.append(question.type)
        all_questions.append([true_false_list, yes_no_list, textbox_list, matching_heading_list,
                              matching_paragraph_list, summary_completion_list, radiobutton_list, checkbox_list])
        question_type.append(temp_type)
        all_questions[i].sort()
        i += 1

    empty = []
    for j in range(len(all_questions)):
        for z in range(len(all_questions[j])):
            if empty in all_questions[j]:
                all_questions[j].remove(empty)

    len_passages = 0
    questions_types = []
    question_type_zip = zip(all_questions, question_type)
    for questions, types in question_type_zip:
        question_type_dict = {}
        len_passages += 1
        for i in range(len(questions)):
            question_type_dict[types[i]] = questions[i]
        questions_types.append(question_type_dict)

    prev_len = 0
    number_of_questions = []
    start_point = 1
    for question in questions_types:
        number_of_questions_dic = {}
        for key in question:
            if start_point == len(question[key]) + prev_len:
                number_of_questions_dic[key] = str(start_point)
            else:
                number_of_questions_dic[key] = str(start_point) + '-' + str(len(question[key]) + prev_len)
            prev_len += len(question[key])
            start_point += len(question[key])
        number_of_questions.append(number_of_questions_dic)
    # print(questions_types)
    # get text in html form then render it

    templates = []
    for passage in all_passages:
        html_for_passage = str(passage.text)
        template = loader.get_template(html_for_passage).render()
        print(type(template))
        templates.append(template)

    passage_question_type_count = zip(all_passages, questions_types, questions_bound, number_of_questions, templates)

    context = {
        'refresh_checker': user_answer + 1,
        'current_exam': current_exam,
        'passage_question_type_count': passage_question_type_count,
        'len_passages': len_passages,
    }
    return render(request, 'Reading/passages.html', context=context)


# calculate grade and submit comments
@login_required(login_url="/login")
def submit(request, exam_id):
    # calculate grade
    if request.POST.get('Submit'):
        # get passage and question
        current_exam = models.Exam.objects.get(id=exam_id)

        all_passages = models.Passage.objects.filter(exam=current_exam).order_by('priority')
        all_questions = []
        for passage in all_passages:
            all_questions.extend(models.Question.objects.filter(passage=passage).order_by('priority'))

        refresh_checker = request.POST.get('refresh_checker')

        all_answers = []
        correct_answers = []

        grade = 0

        # get user answers
        # get  user answer id of questions
        for question in all_questions:
            if question.type == 'truefalse':
                answer_id = request.POST.get('q' + str(question.id))
                all_answers.append(answer_id)

            elif question.type == 'text':
                answer_text = request.POST.get('q' + str(question.id))
                all_answers.append(answer_text)

            elif question.type == 'radiobutton':
                answer_id = request.POST.get('q' + str(question.id))
                all_answers.append(answer_id)

            elif question.type == 'checkbox':
                answer_id = request.POST.getlist('q' + str(question.id))
                all_answers.append(answer_id)

        # calculate correct answers and grade
        for question, answer in zip(all_questions, all_answers):
            if question.type == 'truefalse':
                if answer:
                    my_answer = get_object_or_404(models.Answer, id=answer).truth
                    if my_answer:
                        correct_answers.append(question.id)
                        grade += 1
            elif question.type == 'text':
                if answer == get_object_or_404(models.Answer, question=question.id).text:
                    correct_answers.append(question.id)
                    grade += 1
            elif question.type == 'radiobutton':
                if answer:
                    my_answer = get_object_or_404(models.Answer, id=answer).truth
                    if my_answer:
                        correct_answers.append(question.id)
                        grade += 1
            elif question.type == 'checkbox':
                count_q = 0
                answers_q = get_list_or_404(models.Answer, question=question)
                for ans in answers_q:
                    if ans.truth:
                        count_q += 1
                for ans in answer:
                    if get_object_or_404(models.Answer, id=ans).truth:
                        count_q -= 1
                    else:
                        count_q += 1
                if count_q == 0:
                    correct_answers.append(question.id)
                    grade += 1

        multi_number = 100 / len(all_questions)
        final_grade = grade * multi_number
        final_grade = round(final_grade, 2)

        # create a json from answers
        len_all_questions = len(all_questions)
        save_list = {}
        for question, i in zip(all_questions, range(len_all_questions)):
            if question.id in correct_answers:
                save_list[str(i+1)] = "correct"
            else:
                save_list[str(i+1)] = "wrong"

        print(save_list)
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
            'all_passages': all_passages,
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
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
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
            user = authenticate(request, username=username, password=password)
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('Reading:home')
    else:
        return render(request, 'Reading/signup.html')


# show and filter exams
def exam(request):
    # check method
    if request.POST:
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
        # check if we have filter by category
        if len(filter_category) > 0:
            exams = models.Exam.objects.filter(category__in=filter_category)
        # check if we have filter by difficulty
        if len(filter_difficulty) > 0:
            exams = models.Exam.objects.filter(difficulty__in=filter_difficulty)
        # if don't chose any filter then select all exams
        if len(filter_difficulty) == 0 and len(filter_category) == 0:
            exams = get_list_or_404(models.Exam)

        exam_filter = models.Exam

        # create context
        context = {
            'exam_filter': exam_filter,
            'exams': exams,
        }
        return render(request, 'Reading/filter.html', context=context)
    else:
        books = get_list_or_404(models.Book)
        exam_filter = models.Exam
        context = {
            'books': books,
            'exam_filter': exam_filter,
        }
        return render(request, 'Reading/filter.html', context=context)
