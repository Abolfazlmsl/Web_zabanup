from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField(primary_key=True)
    address = models.TextField()

    def __str__(self):
        return '{}, {}'.format(self.user.first_name, self.user.last_name)


class Passage(models.Model):
    # pk slang
    title = models.CharField(max_length=200)
    text = models.TextField()

    def __str__(self):
        return self.title


class Question(models.Model):
    passage = models.ForeignKey(Passage, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=700)

    def __str__(self):
        return '%s' % self.id


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=300)
    truth = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.id


class UserAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True)
