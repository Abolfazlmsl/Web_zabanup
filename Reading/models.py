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
    text = models.FileField()
    image = models.FileField()

    def __str__(self):
        return self.title


class Exam(models.Model):
    BOOK_List = [
        ('oxford', 'Oxford'),
        ('cambridge', 'Cambridge')
    ]
    CATEGORY = [
        ('politic', 'Politic'),
        ('scientific', 'Scientific'),
        ('economic', 'Economic'),
        ('sport', 'Sport'),
        ('biography', 'Biography'),
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
    image = models.FileField(null=True, blank=True)
    reading = models.OneToOneField('Passage', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return '{}, {}'.format(self.book, self.reading)


class Question(models.Model):
    CHOICES = [
        ('dropdown', 'Dropdown'),
        ('text', 'Text'),
        ('radiobutton', 'Radiobutton'),
        ('checkbox', 'Checkbox'),
    ]
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE)
    text = models.CharField(max_length=700)
    type = models.CharField(max_length=32, choices=CHOICES)

    def __str__(self):
        return '%s' % self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=300)
    truth = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.question


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE)
    answer = models.TextField()
    grade = models.FloatField()
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}, {}, {}, {}, {}'.format(str(self.user), str(self.passage), str(self.grade), str(self.answer),
                                           str(self.time))
