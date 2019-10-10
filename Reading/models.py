from django.contrib.auth.models import User
from django.db import models


# User profile model
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
    image = models.FileField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.book)


# Passage model
class Passage(models.Model):
    title = models.CharField(max_length=200)
    text = models.FileField()
    image = models.FileField()
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    priority = models.PositiveIntegerField()

    def __str__(self):
        return self.title


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
