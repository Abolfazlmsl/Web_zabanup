from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from rest_framework import generics
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

