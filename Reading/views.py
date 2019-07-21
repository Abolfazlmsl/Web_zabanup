from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, reverse, get_object_or_404, redirect, get_list_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from . import models
# Create your views here.


def home(request):
    if request.user:
        username = request.user.username
        return render(request, 'home.html', context={'user': username})
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
    print(dropdown)
    print(textbox)
    print(radiobutton)
    print(checkbox)
    context = {
        'passage': passage,
        'dropdown': dropdown,
        'textbox': textbox,
        'radiobutton': radiobutton,
        'checkbox': checkbox,
        'counter': 0,
        'plus': 1,
    }
    return render(request, 'Reading/passages.html', context=context)


# def submit(request, passage_id):
#     if request.method == 'POST':
#         answer_list = []
#         answer_text = []
#         correct_answers = []
#         passage = get_object_or_404(models.Passage, pk=passage_id)
#
#         q1 = request.POST.get('q1')
#         answer_list.append(q1)
#         q2 = request.POST.get('q2')
#         answer_list.append(q2)
#         q3 = request.POST.get('q3')
#         answer_list.append(q3)
#         q7 = request.POST.get('q7')
#         answer_list.append(q7)
#         q8 = request.POST.get('q8')
#         answer_list.append(q8)
#         q9 = request.POST.get('q9')
#         answer_list.append(q9)
#
#         hidden1 = request.POST.get('hidden1')
#         hidden2 = request.POST.get('hidden2')
#         hidden3 = request.POST.get('hidden3')
#         q4 = request.POST.get('q4')
#         q5 = request.POST.get('q5')
#         q6 = request.POST.get('q6')
#         answer_text.append([hidden1, q4])
#         answer_text.append([hidden2, q5])
#         answer_text.append([hidden3, q6])
#
#         q10 = request.POST.getlist('q10')
#         q10_id = request.POST.get('q10_id')
#         print(answer_list)
#         print(answer_text)
#         grade = 0
#         for answer in answer_list:
#             if answer:
#                 my_answer = get_object_or_404(models.Answer, id=answer).truth
#                 if my_answer:
#                     correct_answers.append(get_object_or_404(models.Answer, id=answer).question_id)
#                     grade += 1
#
#         for answer in answer_text:
#             # my_question = models.Question.objects.get(id=answer[0])
#             if answer[1] == get_object_or_404(models.Answer, question=answer[0]).text:
#                 correct_answers.append(int(answer[0]))
#                 grade += 1
#
#         count_q10 = 0
#         answers_10 = models.Answer.objects.filter(question=q10_id)
#         for answer in answers_10:
#             if answer.truth:
#                 count_q10 += 1
#         for answer in q10:
#             if get_object_or_404(models.Answer, id=answer).truth:
#                 count_q10 -= 1
#         if count_q10 == 0:
#             correct_answers.append(int(q10_id))
#             grade += 1
#         print(correct_answers)
#         context = {
#             'List': answer_list,
#             'passage': passage,
#             'grade': grade*10,
#             'correct_answers': correct_answers,
#         }
#         return render(request, 'Reading/submit.html', context)


def submit(request, passage_id):
    if request.method == 'POST':
        passage = get_object_or_404(models.Passage, pk=passage_id)
        questions = get_list_or_404(models.Question, passage=passage)
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
        print(dropdown_list)
        print(textbox_list)
        print(radiobutton_list)
        print(checkbox_list)
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
            answers_q = models.Answer.objects.filter(question=i[0])
            j = i[1]
            for j in answers_q:
                print(j)
                if j.truth:
                    count_q += 1
            for answer in i[0]:
                if get_object_or_404(models.Answer, id=answer).truth:
                    count_q -= 1
            if count_q == 0:
                correct_answers.append(int(i[0]))
                grade += 1
        context = {
                    'passage': passage,
                    'grade': grade*10,
                    'correct_answers': correct_answers,
                    }
        print(grade)
        return render(request, 'Reading/submit.html', context)
    else:
        return redirect('Reading:Reading')


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
