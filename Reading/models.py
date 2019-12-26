import os
from django.contrib.auth.models import User
from django.db import models
from sorl.thumbnail import ImageField

# User profile model
from ckeditor.fields import RichTextField


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11)
    address = models.TextField()

    def __str__(self):
        return '{}, {}'.format(self.user.first_name, self.user.last_name)


class Book(models.Model):
    name = models.CharField(max_length=100)
    rate = models.CharField(max_length=10, blank=True, null=True)
    date = models.DateField(auto_now=True)
    test_taken = models.IntegerField(blank=True, null=True)
    image = ImageField(upload_to='../media/', null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name)


class ExamCategory(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return '{}'.format(self.name)


class Exam(models.Model):

    DIFFICULTY = [
        ('beginner', 'Beginner'),
        ('pre_intermediate', 'Pre intermediate'),
        ('intermediate', 'Intermediate'),
        ('upper_intermediate', 'Upper intermediate'),
        ('advanced', 'Advanced'),
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    category = models.ManyToManyField(ExamCategory)
    difficulty = models.CharField(max_length=32, choices=DIFFICULTY)

    def __str__(self):
        return '{}, {}, {}'.format(self.book, self.category, self.difficulty)

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
    text = RichTextField()
    image = ImageField(upload_to='../media/')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    priority = models.PositiveIntegerField()

    def __str__(self):
        return self.title


# @receiver(models.signals.post_delete, sender=Passage)
# def auto_delete_file_on_delete(sender, instance, **kwargs):
#
#     if instance.text:
#         if os.path.isfile(instance.text.path):
#             os.remove(instance.text.path)
#
#     if instance.image:
#         if os.path.isfile(instance.image.path):
#             os.remove(instance.image.path)
#
#
# @receiver(models.signals.pre_save, sender=Passage)
# def auto_delete_file_on_change(sender, instance, **kwargs):
#
#     if not instance.pk:
#         return False
#
#     try:
#         old_file = Passage.objects.get(pk=instance.pk).text
#     except Passage.DoesNotExist:
#         return False
#
#     new_file = instance.text
#     if not old_file == new_file:
#         if os.path.isfile(old_file.path):
#             os.remove(old_file.path)


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
    description = models.CharField(max_length=200)

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


# Favorite Question of a User Model
class FavoriteQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{}, {}'.format(self.user, self.question)


# Ticket Model
class Ticket(models.Model):
    CHOICES = [
        ('practice', 'تمرین و آموزش'),
        ('exam', 'آزمون'),
        ('support', 'پشتیبانی'),
        ('Sale', 'فروش'),
    ]
    title = models.CharField(max_length=90, blank=False)
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='staff', null=True)
    student = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='student', null=True)
    date = models.DateTimeField(auto_now=True)
    relate_unit = models.CharField(max_length=128, choices=CHOICES)

    def str(self):
        return '{}, {}, {}, {}'.format(self.title, self.relate_unit, self.staff, self.student)


# Messages of a Ticket model
class TicketMessage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField(blank=False)
    time = models.DateTimeField(auto_now=True)

    def str(self):
        return '{}, {}'.format(self.ticket, self.text)


# Chat Model
class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='sender', null=True)
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='receiver', null=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}, {}, {}'.format(self.sender, self.receiver, self.id)


# Messages of a Chat Model
class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField(blank=False)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}, {}, {}'.format(self.chat, self.sender, self.text)
