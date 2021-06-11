from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import datetime


GENDER_CHOICE = (
    (0, "female"),
    (1, "male")
)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date_published')
    # pub_date = models.DateTimeField('date_published', null=True)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    # def was_published_recently(self):
    #     now = timezone.now()
    #     return now - datetime.timedelta(days=1) <= self.pub_date <= now
    #     # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class MyTestClass(models.Model):
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    choice_text_2 = models.CharField(max_length=200)
    votes_2 = models.IntegerField(default=0)


class Name(models.Model):
    who_add = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    gender = models.IntegerField(choices=GENDER_CHOICE)

    def __str__(self):
        return "{0} {1}".format(self.name, self.surname)
