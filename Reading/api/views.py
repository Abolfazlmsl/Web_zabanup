from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from . import permissons
from Reading import models
from . import serializers
from Crypto.Cipher import AES


class ExamList(generics.ListAPIView):
    # permission_classes = (IsAdminUser, IsAuthenticatedOrReadOnly)

    serializer_class = serializers.ExamSerializers

    def get_queryset(self):
        query = models.Exam.objects.all()

        book = self.request.GET.get('book')
        category = self.request.GET.get('category')
        difficulty = self.request.GET.get('difficulty')

        if book is not None:
            book_list = book.split(",")
            query = query.filter(book__in=book_list)
        if category is not None:
            category_list = category.split(",")
            query = query.filter(category__in=category_list)
        if difficulty is not None:
            difficulty_list = difficulty.split(',')
            query = query.filter(difficulty__in=difficulty_list)

        return query


class ExamDetail(generics.RetrieveAPIView):
    queryset = models.Exam.objects.all()
    serializer_class = serializers.ExamDetailSerializers


class UserAnswerList(generics.ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.UserAnswerListSerializer

    def get_queryset(self):
        query = models.UserAnswer.objects.all()

        exam = self.request.GET.get('exam')
        user = self.request.GET.get('user')

        if exam is not None:
            query = query.filter(exam=exam)
        if user is not None:
            query = query.filter(user=user)

        return query


class UserAnswerCreate(generics.CreateAPIView):
    permission_classes = (permissons.CurrentUserAnswerPermission,)
    serializer_class = serializers.UserAnswerSerializer
    queryset = models.UserAnswer.objects.all()


class UserAnswerDetail(generics.RetrieveAPIView):
    permission_classes = (permissons.CurrentUserAnswerPermission,)
    queryset = models.UserAnswer.objects.all()
    serializer_class = serializers.UserAnswerSerializer


class UserList(generics.ListAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = serializers.UserSerializer
    queryset = User.objects.filter(is_superuser=False)


class UserCreate(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissons.CurrentUserPermission,)
    serializer_class = serializers.UserSerializer
    queryset = User.objects.filter(is_superuser=False)


class ProfileCreate(generics.CreateAPIView):
    serializer_class = serializers.ProfileSerializer
    queryset = models.Profile.objects.all()


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissons.CurrentProfilePermission,)
    serializer_class = serializers.ProfileSerializer
    lookup_field = 'user'
    queryset = models.Profile.objects.all()


class CommentList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        query = models.Comment.objects.all()

        exam = self.request.GET.get('exam')
        user = self.request.GET.get('user')

        if exam is not None:
            query = query.filter(exam=exam)
        if user is not None:
            query = query.filter(user=user)

        return query


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()


class AnswerList(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        answer_json = {}
        exam = models.Exam.objects.get(id=self.kwargs['exam'])
        passages = models.Passage.objects.filter(exam=exam)
        for passage in passages:
            questions = models.Question.objects.filter(passage=passage)
            for question in questions:
                answers = models.Answer.objects.filter(question=question, truth=True)
                if len(answers) > 1:
                    temp = []
                    for answer in answers:
                        temp.append(answer.id)
                    answer_json[question.id] = temp
                else:
                    for answer in answers:
                        if question.type == 'text':
                            answer_json[question.id] = answer.text
                        else:
                            answer_json[question.id] = answer.id
        res = str(answer_json)
        res = pad(res)
        key = '4428472D4B6156045367566B59703373'
        return HttpResponse(str(aes_encrypt(res, key)))
# aes_decrypt(aes_encrypt(res, key), key)


def pad(text):
    while len(text) % 16 != 0:
        text += ' '
    return text


def aes_encrypt(text, key):
    cipher = AES.new(key)
    cipher_text = cipher.encrypt(text)
    return cipher_text


@api_view(['get'])
def book(request):
    exam_detail_json = {}
    question_type_filter = request.GET.get('question_type')
    category_filter = request.GET.get('category')
    book_filter = request.GET.get('book')

    # check user want filter exams or not
    if not book_filter and not category_filter and not question_type_filter:
        # book part
        all_books = models.Book.objects.all()
        book_list = []
        for t_book in all_books:
            temp_dictionary = {
                "id": t_book.id,
                "name": t_book.name,
                "image": t_book.image.url
            }
            book_list.append(temp_dictionary)
        exam_detail_json['book'] = book_list

        # categories part
        all_categories = models.ExamCategory.objects.all()
        category_list = []
        for category in all_categories:
            temp_dictionary = {
                "id": category.id,
                "name": category.name
            }
            category_list.append(temp_dictionary)
        exam_detail_json['category'] = category_list

        # question type part
        question_type = models.Question.CHOICES
        type_list = []
        for qt in question_type:
            temp_dictionary = {
                "name": qt[0],
                "value": qt[1]
            }
            type_list.append(temp_dictionary)
        exam_detail_json['question_type'] = type_list

        # passage type part
        exam_detail_json['passage_type'] = []

    # exam part
    all_exams = models.Exam.objects.all()
    if book_filter:
        all_exams.filter(book_id=book_filter)
    if category_filter:
        all_exams.filter(category_id=category_filter)
    if question_type_filter:
        all_exams.filter(passage__question__type__in=question_type_filter)
    exam_list = []
    for exam in all_exams:
        first_passage = models.Passage.objects.get(exam=exam, priority=1)
        temp_dictionary = {
            "id": exam.id,
            "book": exam.book_id,
            "name": first_passage.title,
            "image": first_passage.image.url,
            "categories": [],
            "questions_type": [],
        }
        for category in exam.category.all():
            temp_dictionary_sec = {
                'id': category.id,
                'name': category.name
            }
            temp_dictionary["categories"].append(temp_dictionary_sec)
        temp = []
        all_passages = models.Passage.objects.filter(exam=exam)
        for passage in all_passages:
            all_questions = models.Question.objects.filter(passage=passage)
            for question in all_questions:
                if question.type not in temp:
                    temp.append(question.type)
                    temp_dictionary_sec = {
                        'name': question.type
                    }
                    temp_dictionary["questions_type"].append(temp_dictionary_sec)
        exam_list.append(temp_dictionary)
    exam_detail_json['exams'] = exam_list

    return JsonResponse(exam_detail_json, safe=False)
