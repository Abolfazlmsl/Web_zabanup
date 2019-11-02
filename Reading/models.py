import os
from django.contrib.auth.models import User
from django.core import serializers
from django.db import models
from sorl.thumbnail import ImageField


# User profile model
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.forms import model_to_dict
from django.http import JsonResponse


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(primary_key=True, max_length=11)
    address = models.TextField()

    def __str__(self):
        return '{}, {}'.format(self.user.first_name, self.user.last_name)


# Exam model
class Exam(models.Model):
    BOOK_List = [
        ('oxford', 'Oxford'),
        ('cambridge', 'Cambridge')
    ]
    CATEGORY = [
        ('education', 'Education'),
        ('science', 'Science'),
        ('economic', 'Economic'),
        ('sport', 'Sport'),
        ('nature_and_environment', 'Nature and Environment'),
        ('technology', 'Technology'),
    ]
    DIFFICULTY = [
        ('beginner', 'Beginner'),
        ('pre_intermediate', 'Pre intermediate'),
        ('intermediate', 'Intermediate'),
        ('upper_intermediate', 'Upper intermediate'),
        ('advanced', 'Advanced'),
    ]
    book = models.CharField(max_length=32, choices=BOOK_List)
    category = models.CharField(max_length=32, choices=CATEGORY)
    difficulty = models.CharField(max_length=32, choices=DIFFICULTY)
    image = ImageField(upload_to='../media/', null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.book)

    def get_api_passage(self):
        passage_question_answer = []
        passages = Passage.objects.filter(exam=self.id).values('id', 'title', 'text', 'image', 'priority')
        for passage in passages:
            temp_dict = passage
            questions = Question.objects.filter(passage=passage['id']).values('id', 'text', 'type', 'priority')
            temp_dict['question'] = []
            i = 0
            for question in questions:
                temp_dict['question'].append(question)
                answers = Answer.objects.filter(question=question['id']).values('id', 'text')
                temp_dict['question'][i]['answer'] = []
                for answer in answers:
                    if question['type'] == 'text':
                        temp_dict['question'][i]['answer'].append({
                                                                    'id': answer['id'],
                                                                    'text': '',
                                                                  })
                    else:
                        temp_dict['question'][i]['answer'].append(answer)
                i += 1
            passage_question_answer.append(temp_dict)
        return passage_question_answer


# Passage model
class Passage(models.Model):
    title = models.CharField(max_length=200)
    text = models.FileField()
    image = ImageField(upload_to='../media/')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    priority = models.PositiveIntegerField()

    def __str__(self):
        return self.title


@receiver(models.signals.post_delete, sender=Passage)
def auto_delete_file_on_delete(sender, instance, **kwargs):

    if instance.text:
        if os.path.isfile(instance.text.path):
            os.remove(instance.text.path)

    # if instance.image:
    #     if os.path.isfile(instance.image.path):
    #         os.remove(instance.image.path)


@receiver(models.signals.pre_save, sender=Passage)
def auto_delete_file_on_change(sender, instance, **kwargs):

    if not instance.pk:
        return False

    try:
        old_file = Passage.objects.get(pk=instance.pk).text
    except Passage.DoesNotExist:
        return False

    new_file = instance.text
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


# Question model
class Question(models.Model):
    CHOICES = [
        ('dropdown', (('truefalse', 'TrueFalse'), ('yesno', 'YesNo'))),
        ('text', 'Text'),
        ('matching_heading', 'Matching Heading'),
        ('matching_paragraph', 'Matching Paragraph'),
        ('summary_completion', 'Summary Completion'),
        ('radiobutton', 'Radiobutton'),
        ('checkbox', 'Checkbox'),
    ]
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE)
    text = models.CharField(max_length=700)
    type = models.CharField(max_length=32, choices=CHOICES)
    priority = models.PositiveIntegerField()

    def __str__(self):
        return '%s' % self.text


# Answers of Question model
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=300)
    truth = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.question


# Answer that user choose model
class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    answer = models.TextField()
    grade = models.FloatField()
    time = models.DateTimeField(auto_now=True)
    counter = models.IntegerField()

    def __str__(self):
        return '{}, {}, {}, {}, {}'.format(str(self.user), str(self.exam), str(self.grade), str(self.answer),
                                           str(self.time))


# Comment model
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}, {}, {}, {}'.format(self.id, self.user, self.text, self.parent_id)
