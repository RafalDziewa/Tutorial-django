from polls.models import Choice, Question
from django.utils import timezone
q = Question(question_text="What's new?", pub_date=timezone.now())
q.save()
q.id
q.question_text
q.pub_date
q.question_text = "What's up?"
q.save()
Question.objects.all()


import datetime
from django.utils import timezone
from polls.models import Question


from django.test.utils import setup_test_environment
setup_test_environment()
from django.test import Client
client = Client()


class Name(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    def __str__(self):
        return self.name

        <!--<form action="{% url 'polls:{{ name_url }}' name_id %}" method="post">-->
